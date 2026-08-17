# Checklist: Aktualizace existujícího Kodi doplňku

Postup pro vydání nové verze doplňku, který už v repozitáři CzechGod je.
Nahrazuj `<id>` skutečným ID doplňku (např. `plugin.video.kowesha`),
`<stará_verze>` původní a `<nová_verze>` novou verzí (např. `0.2.1` → `0.2.2`).

## 1. Bumpni verzi v `addon.xml`

- [ ] Ve složce doplňku uprav `version` v `<id>/addon.xml` na `<nová_verze>`.
- [ ] Pokud má doplněk externí zdroj (např. `/projects/kowesha`),
  bumpni verzi i tam a udrž `addon.xml` synchronní se zdrojem.
- [ ] Bez změny verze Kodi aktualizaci nenabídne a generátor nevytvoří nový ZIP.

## 2. Vlož nový ZIP `<id>/<id>-<nová_verze>.zip`

Máš dvě možnosti (stejně jako u přidání):

- [ ] **A) Nech ZIP sestavit generátor** – aktualizuj obsah složky `<id>/`
  (nové `addon.xml`, změněné `resources/`/kód) a `just build` sestaví
  chybějící `<id>/<id>-<nová_verze>.zip` z obsahu složky.
- [ ] **B) Zkopíruj hotový ZIP** – zkopíruj připravený archiv do
  `<id>/<id>-<nová_verze>.zip`. Ověř, že kořenová složka uvnitř je `<id>/`
  (`unzip -l <id>/<id>-<nová_verze>.zip`).

## 3. Odstraň starou ZIP verzi

- [ ] Smaž `<id>/<id>-<stará_verze>.zip`:
  ```bash
  rm <id>/<id>-<stará_verze>.zip
  ```
- [ ] Důvod: `_repo_generator.py` sestaví jen **chybějící** archiv a existující
  nepřepisuje. Kdybys starý ZIP nechal, zůstal by v repu vedle nové verze
  jako neaktuální balík.

## 4. Spusť `just build`

- [ ] Spusť v kořeni repozitáře:
  ```bash
  just build
  ```
- [ ] Ve výstupu ověř, že u doplňku je uvedena `<nová_verze>` a archiv je
  `built` (nově sestaven) pro novou verzi.

## 5. Ověř novou verzi a shodu MD5

- [ ] `addons.xml` obsahuje u doplňku `version="<nová_verze>"` (ne starou).
- [ ] MD5 sedí:
  ```bash
  md5sum addons.xml
  cat addons.xml.md5
  ```
  Oba řetězce musí být shodné.
- [ ] Ve složce `<id>/` je jen nový `<id>-<nová_verze>.zip`
  a starý `<id>-<stará_verze>.zip` už tam není:
  ```bash
  ls <id>/*.zip
  ```

## 6. Aktualizuj dokumentaci (`README.md`, případně `index.html`)

- [ ] V tabulce „Dostupné doplňky" v `README.md` uprav sloupec verze u doplňku
  na `<nová_verze>`.
- [ ] **Jen když aktualizuješ samotné repository (`<id>` = `repository.czechgod`):**
  přepiš i cestu k bootstrap ZIPu na `repository.czechgod-<nová_verze>.zip`:
  - v `README.md` v kroku „Install from zip file",
  - v `index.html` (kořen repozitáře) na **obou** místech
    (`<a href="…">` i `<div class="url">`).
- [ ] Ověř, že nikde nezůstal odkaz na `repository.czechgod-<stará_verze>.zip`.

## 7. Commit + push

- [ ] Zkontroluj změny (`git status`): `<id>/addon.xml`, nový ZIP, smazaný
  starý ZIP, `addons.xml`, `addons.xml.md5`, `README.md` (a při bumpu
  `repository.czechgod` i `index.html`).
- [ ] Zacommituj a pushni – GitHub Pages katalog zveřejní novou verzi a Kodi
  ji nabídne k automatické aktualizaci.

## Časté chyby

- **Zapomenutý bump verze** v `addon.xml` (nejčastější chyba u aktualizace).
- **Ponechaná stará `<id>-<stará_verze>.zip`** – vždy ji smaž.
- **Zapomenutý odkaz na bootstrap ZIP** při bumpu `repository.czechgod` –
  aktualizuj cestu i v `README.md` a na obou místech v `index.html`.
- Špatná kořenová složka uvnitř nového ZIPu (musí být `<id>/`).
- Nespuštěný `just build` → neaktuální `addons.xml`/`addons.xml.md5`.
- Ruční editace generovaných `addons.xml`/`addons.xml.md5`.
