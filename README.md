# AIBox — Project Cost Management

A Django-based construction project cost management system with Jazzmin Admin interface.

---

## Project Structure

```
techycloud9/
├── core/                   # Django configuration (settings, urls, wsgi)
├── main/                   # Master data: projects, partners, banks, accounting categories
├── opening/                # Opening balances per accounting account
├── voucher/                # Vouchers: purchase invoices, receipts, payments, bank notices
├── ledger/                 # General ledger, detailed account ledger
├── report/                 # Reports: receivables, payables, cash payment summary
├── info/                   # Company info, user guide
├── templates/              # HTML templates
│   ├── admin/              # Django Admin overrides (index, login)
│   ├── voucher/            # Voucher print templates
│   ├── ledger/             # Ledger view templates
│   ├── report/             # Report templates
│   ├── info/               # Company info templates
│   └── file_templates/     # Word (.docx) export templates
├── static_dir/             # Static files (CSS, JS, images)
├── locale/                 # Translation files (EN / VI)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
```

### Apps

| App | Description |
|-----|-------------|
| `main` | Master data: projects, partners, banks, company bank accounts, accounting categories |
| `opening` | Opening balances per accounting account |
| `voucher` | Purchase invoices, receipts, payments, debit/credit bank notices |
| `ledger` | General ledger and detailed account ledger — view and export to Word |
| `report` | Receivables report, payables report, cash payment summary — export to Word |
| `info` | Company information, user guide |

---

## Requirements

- Docker & Docker Compose

---

## Running with Docker Compose

### 1. Clone the repository

```bash
git clone <repo-url>
cd techycloud9
```

### 2. Start the application

```bash
docker compose up --build
```

On first run, Docker will automatically:
- Install dependencies from `requirements.txt`
- Run `migrate` to initialize the database
- Start the server on port `8000`

### 3. Create an admin account

Open a new terminal while the container is running:

```bash
docker compose exec web python manage.py createsuperuser
```

### 4. (Optional) Seed sample data

```bash
docker compose exec web python manage.py seed
```

### 5. Access

| URL | Description |
|-----|-------------|
| http://localhost:8000/admin/ | Admin panel |

---

## Stopping the application

```bash
docker compose down
```

To also remove all data (database):

```bash
docker compose down -v
```

---

## Running without Docker (optional)

```bash
python3.8 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## Key Settings

| Setting | Value |
|---------|-------|
| Database | SQLite (`db.sqlite3`) |
| Admin theme | Jazzmin |
| Languages | English, Vietnamese |
| Export format | Word (.docx) via docxtpl |
