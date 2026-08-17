#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the Kodi repository catalog (``addons.xml`` + ``addons.xml.md5``).

A Kodi repository published via GitHub Pages needs:

* for every add-on a ``<id>/`` folder with the installable archive
  ``<id>/<id>-<version>.zip`` (because ``datadir`` has ``zip="true"``),
* an ``addons.xml`` file with the merged ``addon.xml`` of all add-ons,
* an ``addons.xml.md5`` file with the MD5 checksum of ``addons.xml``.

This script:

* scans the repository's direct subdirectories that contain ``addon.xml``,
* reads the ``id`` and ``version`` from each ``addon.xml``,
* if the ``<id>/<id>-<version>.zip`` archive is missing, builds it from the
  folder contents (skipping development/helper files) so the add-on can be
  installed from the repository,
* assembles ``addons.xml`` and writes ``addons.xml.md5``.

Uses only the Python standard library, so it requires no external tools.

Usage::

    python3 _repo_generator.py
"""

import argparse
import fnmatch
import hashlib
import os
import sys
import xml.etree.ElementTree as ET
import zipfile

# Repository root = the directory this script lives in.
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
ADDONS_XML = os.path.join(REPO_ROOT, "addons.xml")
ADDONS_XML_MD5 = os.path.join(REPO_ROOT, "addons.xml.md5")

# Directory names that never end up in an add-on's installable archive.
EXCLUDE_DIRS = {
    ".git",
    ".idea",
    ".junie",
    ".venv",
    "venv",
    "tests",
    "dist",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
}

# File patterns that never end up in an add-on's installable archive.
EXCLUDE_FILE_PATTERNS = (
    ".gitignore",
    ".gitattributes",
    ".DS_Store",
    "Thumbs.db",
    "*.iml",
    "*.py[cod]",
    "*.log",
    "*.zip",
)


def read_addon_metadata(addon_xml):
    """Return (id, version) from ``addon.xml``.

    Raises a clear error when the file is not valid XML or is missing the
    required attributes.
    """
    try:
        root = ET.parse(addon_xml).getroot()
    except ET.ParseError as exc:
        raise SystemExit("Error: {0} is not valid XML: {1}".format(addon_xml, exc))

    addon_id = root.get("id")
    version = root.get("version")
    if not addon_id or not version:
        raise SystemExit(
            "Error: attribute 'id' or 'version' missing in {0}.".format(addon_xml)
        )
    return addon_id, version


def is_excluded_file(name):
    """True if the file name matches one of the excluded patterns."""
    return any(fnmatch.fnmatch(name, pat) for pat in EXCLUDE_FILE_PATTERNS)


def collect_files(root):
    """Walk the add-on tree and return a sorted list of relative paths to pack."""
    collected = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for filename in filenames:
            if is_excluded_file(filename):
                continue
            abs_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(abs_path, root)
            collected.append(rel_path)
    collected.sort()
    return collected


def build_addon_zip(addon_dir, addon_id, version):
    """Build ``<id>/<id>-<version>.zip`` from the add-on folder contents."""
    zip_name = "{0}-{1}.zip".format(addon_id, version)
    zip_path = os.path.join(addon_dir, zip_name)

    files = collect_files(addon_dir)
    if "addon.xml" not in files:
        raise SystemExit(
            "Error: addon.xml missing in {0}, cannot build the archive.".format(addon_dir)
        )

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel_path in files:
            abs_path = os.path.join(addon_dir, rel_path)
            # Everything must live under a single root folder named after the ID.
            arcname = os.path.join(addon_id, rel_path)
            zf.write(abs_path, arcname)
    return zip_path


def find_addon_dirs(repo_root):
    """Return a sorted list of subdirectories that contain ``addon.xml``."""
    addon_dirs = []
    for name in sorted(os.listdir(repo_root)):
        path = os.path.join(repo_root, name)
        if not os.path.isdir(path) or name in EXCLUDE_DIRS:
            continue
        if os.path.isfile(os.path.join(path, "addon.xml")):
            addon_dirs.append(path)
    return addon_dirs


def read_addon_xml_body(addon_xml):
    """Return the ``addon.xml`` content without the XML declaration (the root ``<addon>`` element)."""
    with open(addon_xml, "r", encoding="utf-8") as handle:
        text = handle.read()
    # Strip any XML declaration and surrounding whitespace.
    start = text.find("<addon")
    if start == -1:
        raise SystemExit("Error: <addon> element missing in {0}.".format(addon_xml))
    return text[start:].strip()


def generate(repo_root):
    """Build addons.xml + addons.xml.md5 and add any missing add-on archives."""
    addon_dirs = find_addon_dirs(repo_root)
    if not addon_dirs:
        raise SystemExit("Error: no add-on found (a directory with addon.xml).")

    blocks = []
    summary = []
    for addon_dir in addon_dirs:
        addon_xml = os.path.join(addon_dir, "addon.xml")
        addon_id, version = read_addon_metadata(addon_xml)

        zip_name = "{0}-{1}.zip".format(addon_id, version)
        zip_path = os.path.join(addon_dir, zip_name)
        if not os.path.isfile(zip_path):
            build_addon_zip(addon_dir, addon_id, version)
            built = "built"
        else:
            built = "exists"

        blocks.append(read_addon_xml_body(addon_xml))
        summary.append((addon_id, version, built))

    body = "\n".join(blocks)
    addons_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        "<addons>\n" + body + "\n</addons>\n"
    )

    with open(ADDONS_XML, "w", encoding="utf-8") as handle:
        handle.write(addons_xml)

    digest = hashlib.md5(addons_xml.encode("utf-8")).hexdigest()
    with open(ADDONS_XML_MD5, "w", encoding="utf-8") as handle:
        handle.write(digest + "\n")

    return summary, digest


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate addons.xml and addons.xml.md5 for a Kodi repository."
    )
    parser.parse_args(argv)

    summary, digest = generate(REPO_ROOT)

    print("Done: addons.xml + addons.xml.md5")
    for addon_id, version, built in summary:
        print("  {0}  version: {1}  (archive: {2})".format(addon_id, version, built))
    print("  MD5: {0}".format(digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
