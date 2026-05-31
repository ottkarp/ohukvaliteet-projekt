# Edenemisraport (Sprint 2)

## Mis on valmis
- [x] Docker Compose käivitab andmebaasi, Pythoni keskkonna ja Streamlit näidikulaua.
- [x] Andmeid saadakse Open-Meteo Air Quality API-st kätte (hetkel Tallinna PM2.5 andmed).
- [x] Andmed laetakse `staging.air_quality_raw` tabelisse (idempotentselt).
- [x] Transformatsioon arvutab `mart.daily_air_quality` tabelisse, mitu tundi päevas ületab PM2.5 tase WHO piirmäära (15 µg/m³).
- [x] Streamlit näidikulaud kuvab andmebaasist loetud andmete põhjal tulpdiagrammi.

## Järgmised sammud
- Lisada juurde teised linnad (Tartu, Pärnu, Narva) kasutades staatilist asukohtade tabelit.
- Lisada juurde teised saasteained (PM10, Osoon).
- Heija-Liis saab hakata Streamliti näidikulauda ilusamaks ja detailsemaks disainima.
- Lisada andmekvaliteedi testid (Sprint 3 nõue).

## Mis takistab
- Praegu blokeerivaid probleeme pole. Minimaalne toru töötab algusest lõpuni.

## Kontrollpunkt
Käsk, millega saab kontrollida, et töövoog töötab (tõmbab andmed ja teeb arvutused):
```bash
docker compose exec pipeline python scripts/run_pipeline.py
