---
name: manage-kodi-addon
description: Postup pro přidání nového nebo aktualizaci existujícího Kodi doplňku v tomto repository (CzechGod) – struktura <id>/ složky, instalační ZIP, generování addons.xml přes `just build` a verifikace. Použij, když jde o úkol typu „přidej addon" nebo „aktualizuj doplněk".
---

# Správa Kodi doplňků v repository CzechGod

Tato dovednost popisuje ověřený postup pro **přidání nového** i **aktualizaci
existujícího** Kodi doplňku v tomto repozitáři. Repozitář je Kodi add-on
repository publikovaný přes GitHub Pages (`https://czechgod.github.io/kodi-addons/`).

## Kdy použít

Použij tuto dovednost, když máš:

- **přidat nový doplněk** do repozitáře (nová složka `<id>/`, instalační ZIP,
  zaregistrování do katalogu), nebo
- **aktualizovat existující doplněk** (bump verze, nový ZIP, odstranění staré
  verze, regenerace katalogu).

Typické zadání: „přidej addon …", „aktualizuj kowesha na verzi …",
„nahraj novou verzi doplňku".

## Klíčové principy struktury repozitáře

- **Složka doplňku `<id>/`** – každý doplněk má v kořeni repozitáře vlastní
  složku pojmenovanou přesně podle svého ID (např. `plugin.video.kowesha/`).
  Uvnitř je `addon.xml`, `resources/` (např. `icon.png`) a instalační ZIP.
- **Instalační ZIP `<id>/<id>-<version>.zip`** – protože `repository.czechgod/addon.xml`
  má `<datadir zip="true">`, Kodi stahuje doplněk jako archiv na cestě
  `<id>/<id>-<version>.zip` (např. `plugin.video.kowesha/plugin.video.kowesha-0.2.1.zip`).
- **Kořenová složka uvnitř ZIPu = ID doplňku** – archiv musí obsahovat jedinou
  kořenovou složku pojmenovanou přesně jako ID (`plugin.video.kowesha/addon.xml`, …).
  Bez toho Kodi doplněk nenainstaluje.
- **Generátor `_repo_generator.py` sestaví jen CHYBĚJÍCÍ ZIP** – skript projde
  přímé podadresáře s `addon.xml`, přečte `id` + `version` a pokud archiv
  `<id>/<id>-<version>.zip` **chybí**, sestaví ho z obsahu složky (vynechá
  vývojové soubory dle `EXCLUDE_DIRS`/`EXCLUDE_FILE_PATTERNS`). Existující ZIP
  se stejným názvem **nepřepisuje**. Proto se při aktualizaci musí stará ZIP
  verze odstranit ručně (jinak by zůstala v repu vedle nové).
- **`addons.xml` + `addons.xml.md5`** – generátor poskládá `addons.xml` ze
  sloučených `addon.xml` všech doplňků a zapíše MD5 do `addons.xml.md5`.
- **`just build`** – spouští `python3 _repo_generator.py` (cíl `build` → `repo`).
  Je to jediný příkaz, který je potřeba k regeneraci katalogu.

## Přidání nového doplňku

Stručně: vytvoř složku `<id>/` s `addon.xml` + `resources/`, připrav instalační
ZIP `<id>/<id>-<version>.zip` (nebo ho nech sestavit `just build`), spusť
`just build`, ověř katalog a doplň řádek do `README.md`.

Kompletní krok-za-krokem postup je v [`checklists/add.md`](checklists/add.md).

## Aktualizace doplňku

Stručně: bumpni `version` v `<id>/addon.xml`, vlož nový ZIP
`<id>/<id>-<nová_verze>.zip`, **odstraň starou** `<id>/<id>-<stará_verze>.zip`,
spusť `just build`, ověř novou verzi + MD5 a aktualizuj verzi v `README.md`.

Kompletní krok-za-krokem postup je v [`checklists/update.md`](checklists/update.md).

## Verifikace

Po každé změně ověř:

- `just build` proběhne bez chyb a ve výstupu vypíše očekávané `id` + `version`
  každého doplňku (a zda byl archiv `built`/`exists`).
- `addons.xml` je validní XML a obsahuje očekávané verze doplňků.
- MD5 v `addons.xml.md5` odpovídá skutečnému obsahu `addons.xml`
  (`md5sum addons.xml` = obsah `addons.xml.md5`).
- Instalační ZIP `<id>/<id>-<version>.zip` existuje a jeho **kořenová složka
  uvnitř archivu je přesně `<id>/`** (`unzip -l <id>/<id>-<version>.zip`).

## Aktualizace dokumentace

- **`README.md`** – tabulka „Dostupné doplňky" (doplněk, ID, verze, popis).
  Při přidání přidej řádek, při aktualizaci uprav verzi.
- **`../../../index.html`** – návod k instalaci repozitáře; obvykle není potřeba měnit
  při běžném přidání/aktualizaci doplňku (mění se jen při změně cesty k
  bootstrap ZIPu repository).

## Časté chyby (pitfalls)

- **Zapomenutý bump verze** při aktualizaci – Kodi nenabídne aktualizaci a
  generátor neuvidí důvod sestavit nový ZIP.
- **Ponechaná stará `<id>-<stará_verze>.zip`** – zůstane v repu vedle nové
  verze; při aktualizaci ji vždy smaž.
- **Špatná kořenová složka v ZIPu** – archiv nesmí mít soubory přímo v kořeni
  ani vnořenou jinou složku; kořen musí být `<id>/`.
- **Nespuštěný `just build`** – bez regenerace zůstane `addons.xml`/`addons.xml.md5`
  neaktuální a doplněk se v repu neobjeví (nebo v nesprávné verzi).
- **Ruční editace `addons.xml`/`addons.xml.md5`** – nedělej; oba soubory jsou
  generované, uprav zdroj (`addon.xml`) a spusť `just build`.

## Odkazy na soubory v repu

- `_repo_generator.py` – generátor katalogu.
- `justfile` – cíle `build` a `repo`.
- `repository.czechgod/addon.xml` – definice repository (`datadir zip="true"`).
- `plugin.video.kowesha/` – vzorový doplněk (id `plugin.video.kowesha`).
- `README.md`, `../../../index.html` – dokumentace pro uživatele.
