# AIBox — Project Cost Management

Django-based construction project cost management system with admin dashboard.

## Requirements

- Python 3.8
- pip

---

## Setup — Linux

```bash
# 1. Clone the repository
git clone <repo-url>
cd techycloud9

# 2. Create and activate virtual environment
python3.8 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. (Optional) Seed sample data
python manage.py seed

# 7. Run development server
python manage.py runserver
```

Access the admin at: http://127.0.0.1:8000/admin/

---

## Setup — Windows

```powershell
# 1. Clone the repository
git clone <repo-url>
cd techycloud9

# 2. Create and activate virtual environment
py -3.8 -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. (Optional) Seed sample data
python manage.py seed

# 7. Run development server
python manage.py runserver
```

Access the admin at: http://127.0.0.1:8000/admin/

---

## Project Structure

```
techycloud9/
├── core/           # Django project settings and root URLs
├── main/           # Master data: projects, partners, accounts, banks
├── budget/         # Budget planning per project
├── voucher/        # Contracts, invoices, acceptance records, receipts
├── report/         # Custom reports (debt report)
├── templates/      # HTML templates (admin, allauth, dashboard, reports)
├── static_dir/     # Static assets (CSS, images)
├── locale/         # Translation files (EN / VI)
└── manage.py
```

## Apps

| App | Description |
|-----|-------------|
| `main` | Partners, banks, projects, cost categories, opening balances |
| `budget` | Project budget planning and approval |
| `voucher` | Contracts, payment schedules, acceptance records, invoices, receipts, bank notices |
| `report` | Custom report views (not model-based) |

## Key Settings

| Setting | Value |
|---------|-------|
| Database | SQLite (`db.sqlite3`) |
| Admin theme | Jazzmin |
| Authentication | django-allauth (email + Google OAuth) |
| Languages | English, Vietnamese |
| Email | Gmail SMTP (configure `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in `settings.py`) |

## Google OAuth (optional)

In `core/settings.py`, fill in your Google OAuth credentials:

```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '<your-client-id>',
            'secret':    '<your-client-secret>',
        },
    }
}
```

## Translations

After editing `.po` files in `locale/`, compile them:

```bash
python manage.py compilemessages
```
