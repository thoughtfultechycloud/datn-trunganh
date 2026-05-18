# AIBox — Project Cost Management

A Django-based construction project cost management system with Jazzmin Admin interface.

---

## Project Structure

```
datn-trunganh/
├── core/                   # Django configuration (settings, urls, wsgi)
├── main/                   # Master data: projects, partners, banks, accounting categories
├── opening/                # Opening balances per accounting account
├── voucher/                # Vouchers: purchase invoices, receipts, payments, bank notices
├── ledger/                 # General ledger, detailed account ledger
├── report/                 # Reports: receivables, payables, cash payment summary
├── info/                   # Company info, user guide
├── backup/                 # Database backup and restore
├── templates/              # HTML templates
│   ├── admin/              # Django Admin overrides (index, login, backup/restore)
│   ├── voucher/            # Voucher print templates
│   ├── ledger/             # Ledger view templates
│   ├── report/             # Report templates
│   ├── info/               # Company info templates
│   └── file_templates/     # Word (.docx) export templates
├── static_dir/             # Static files (CSS, JS, images)
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
| `backup` | Database backup (`pg_dump`) and restore (`pg_restore`) via admin UI |

---

## Requirements

- Docker & Docker Compose

---

## Running with Docker Compose

### 1. Clone the repository

```bash
git clone <repo-url>
cd datn-trunganh
```

### 2. Configure environment (optional)

Copy the example env file and adjust values if needed:

```bash
cp .env.example .env
```

Default values work out of the box with Docker Compose.

### 3. Start the application

```bash
docker compose up --build
```

On first run, Docker will automatically:
- Build the image (Python 3.8 + postgresql-client)
- Start a **PostgreSQL 15** database container
- Wait for the database to be healthy before starting the web container
- Run `migrate` to initialize the schema
- Start the Django dev server on port `8008`

### 4. Create an admin account

Open a new terminal while the containers are running:

```bash
docker compose exec web python manage.py createsuperuser
```

### 5. (Optional) Seed sample data

```bash
docker compose exec web python manage.py seed
```

Seeds: accounting categories, banks, partners, projects, company bank accounts, user groups, a sample project-manager user, and sample vouchers.

### 6. Access

| URL | Description |
|-----|-------------|
| http://localhost:8008/admin/ | Admin panel |

---

## Stopping the application

```bash
docker compose down
```

To also remove all data (PostgreSQL volume):

```bash
docker compose down -v
```

---

## Running without Docker (optional)

Requires Python 3.8 and a running PostgreSQL 15 instance. Set DB credentials in `.env` or environment variables before running.

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
| Database | PostgreSQL 15 (via Docker) |
| DB credentials | Configured via `.env` (see `.env.example`) |
| Admin theme | Jazzmin |
| Export format | Word (.docx) via docxtpl |
| Backup format | pg_dump custom format (`.dump`) |
