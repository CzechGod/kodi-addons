# Checklist: Přidání nového Kodi doplňku

Postup pro přidání zcela nového doplňku do repozitáře CzechGod.
Nahrazuj `<id>` skutečným ID doplňku (např. `plugin.video.kowesha`)
a `<version>` skutečnou verzí z `addon.xml` (např. `0.2.1`).

## 1. Získej zdroj doplňku

- [ ] Zjisti, odkud pochází doplněk – např. externí projekt
  (jako `/projects/kowesha`), Git repo nebo hotový ZIP.
- [ ] Zjisti přesné `id` a `version` z `addon.xml` zdroje. ID určuje název
  složky i instalačního ZIPu, verze určuje název ZIPu.

## 2. Vytvoř složku doplňku `<id>/`

- [ ] V kořeni repozitáře vytvoř složku pojmenovanou přesně podle ID: `<id>/`.
- [ ] Vlož do ní `addon.xml` doplňku.
- [ ] Vlož `resources/` (minimálně ikonu, typicky `resources/icon.png`,
  pokud na ni `addon.xml` odkazuje v `<assets><icon>`).
- [ ] Nedávej do složky vývojové soubory (`.git`, `.idea`, `.venv`, `tests`,
  `dist`, `__pycache__`, `*.py[cod]`, `*.log`, …) – generátor je sice při
  balení vynechává (viz `EXCLUDE_DIRS`/`EXCLUDE_FILE_PATTERNS` v
  `_repo_generator.py`), ale do repozitáře stejně nepatří.

## 3. Připrav instalační ZIP `<id>/<id>-<version>.zip`

Máš dvě možnosti:

- [ ] **A) Nech ZIP sestavit generátor** – pokud archiv chybí, `just build`
  (resp. `_repo_generator.py`) ho sestaví z obsahu složky `<id>/` a správně
  nastaví kořenovou složku uvnitř archivu na `<id>/`. Tuto variantu preferuj.
- [ ] **B) Zkopíruj hotový ZIP** – pokud už máš připravený instalační archiv
  (např. z externího `build_zip.py`), zkopíruj ho do `<id>/<id>-<version>.zip`.
  Ověř, že jeho kořenová složka uvnitř archivu je přesně `<id>/`
  (`unzip -l <id>/<id>-<version>.zip`).

> Pozor: kořen uvnitř ZIPu musí být jediná složka `<id>/`. Soubory přímo
> v kořeni archivu Kodi odmítne.

## 4. Spusť `just build`

- [ ] Spusť v kořeni repozitáře:
  ```bash
  just build
  ```
- [ ] Zkontroluj výstup – měl by vypsat všechny doplňky s jejich `id`,
  `version` a stavem archivu (`built` = nově sestaven, `exists` = už byl).

## 5. Ověř katalog a strukturu ZIPu

- [ ] `addons.xml` obsahuje blok nového doplňku se správným `id` a `version`.
- [ ] MD5 sedí:
  ```bash
  md5sum addons.xml
  cat addons.xml.md5
  ```
  Oba řetězce musí být shodné.
- [ ] Instalační ZIP existuje a má správný kořen:
  ```bash
  unzip -l <id>/<id>-<version>.zip
  ```
  První úroveň musí být `<id>/…`.

## 6. Doplň řádek do tabulky v `README.md`

- [ ] Do tabulky „Dostupné doplňky" v `README.md` přidej řádek s doplňkem:
  ```markdown
  | <Název> | `<id>` | <version> | <krátký popis> |
  ```

## 7. Commit + push

- [ ] Zkontroluj, které soubory přibyly/změnily se (`git status`):
  složka `<id>/` (s `addon.xml`, `resources/`, ZIP), `addons.xml`,
  `addons.xml.md5`, `README.md`.
- [ ] Zacommituj a pushni – GitHub Pages katalog automaticky zveřejní na
  `https://czechgod.github.io/kodi-addons/`.

## Časté chyby

- Špatná kořenová složka uvnitř ZIPu (musí být `<id>/`).
- Nespuštěný `just build` → neaktuální `addons.xml`/`addons.xml.md5`.
- Ruční editace generovaných `addons.xml`/`addons.xml.md5` (nedělej – uprav
  `addon.xml` a spusť `just build`).
- Zapomenutý řádek v `README.md`.
