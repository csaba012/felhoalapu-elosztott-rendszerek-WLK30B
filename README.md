# Galéria Alkalmazás

Full-stack Galéria alkalmazás Vue.js 3, Flask és PostgreSQL használatával.

## Készítette
Papp Csaba Mihály, WLK30B

## Architektúra

- **Frontend**: Vue.js 3 + Tailwind CSS + FontAwesome
- **Backend**: Flask + SQLAlchemy + JWT authentication
- **Adatbázis**: PostgreSQL
- **Konténerizáció**: Docker + Docker Compose

## Funkciók

### Felhasználókezelés
- Regisztráció
- Belépés
- Kilépés
- JWT alapú autentikáció

### Fényképkezelés
- Fényképek feltöltése (csak bejelentkezett felhasználóknak)
- Fényképek törlése (csak bejelentkezett felhasználóknak)
- Fényképek listázása (csak a saját képek megtekintése)
- Fénykép megtekintése (teljes méret)
- Rendezés név szerint (A-Z, Z-A)
- Rendezés dátum szerint (újabb/régebbi először)