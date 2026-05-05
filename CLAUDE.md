# eizsole.lv — Projekta konteksts

## Kas tas ir
Latvijas marketplace — sludinājumi + izsoles (kā ss.lv + izsolis.lv kopā).
**Izsoles ir prioritāte.**

## Serveris
```powershell
cd C:\Users\USER\izsoles-platforma; venv\Scripts\python.exe manage.py runserver
```
→ http://127.0.0.1:8000/ | Admin: http://127.0.0.1:8000/admin/

## Tech stack
- Django 6.0.4 (Python 3.12) + SQLite
- Bootstrap 5 + Bootstrap Icons + Google Fonts (Inter)
- Templates: `templates/` mapē

## Apps
- `listings/` — sludinājumi, kategorijas (4 līmeņi), moderācija, profanity filter
- `auctions/` — izsoles, solījumi (Bid)
- `accounts/` — login, register, profils

## Svarīgi
- `ALLOWED_HOSTS = ['127.0.0.1', 'localhost']` — obligāts Django 6
- Logout = POST request (ne GET) — Django 6 prasība
- Kategoriju slugi = ASCII (fix_slugs.py pēc jaunām kategorijām)
- Kaskādes dropdown: JS → `/api/subcategories/<pk>/`
- PowerShell lietot (ne bash) — Windows ceļi ar `C:\`

## Pabeigtā funkcionalitāte
- Sludinājumu publicēšana + bildes
- Kategorijas (4 līmeņi, ~12 galvenās + simti apakš)
- Izsoles ar solīšanu
- Admin moderācija (ziņot/deaktivēt/dzēst)
- Profanity filter (LV+EN+RU)
- Aprīkojuma checkboxes Auto sludinājumiem (78 vienumi)
- Meklēšana
- Moderns dizains (2026-04-22)

## Lietotājs
Iesācējs, komunicē **latviski**. Viss jādara Claude pats.
