# Build the whole repository: add-on installable ZIPs + addons.xml + addons.xml.md5
# The repository installable ZIP is produced directly in the repository.czechgod/
# folder (repository.czechgod/repository.czechgod-1.0.0.zip) and is used both for
# the first manual install and for auto-updates – no root-level duplicate is needed.
build: repo

# Generate addons.xml and addons.xml.md5 and add any missing add-on installable ZIPs
repo:
    python3 _repo_generator.py

retrigger:
    git commit --allow-empty -m "trigger build" && git push

checksum-xml:
    curl -fsSL https://czechgod.github.io/kodi-addons/addons.xml | md5sum
checksum-md5:
    curl -fsSL https://czechgod.github.io/kodi-addons/addons.xml.md5.txt
