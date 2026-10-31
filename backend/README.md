# Nugabest CRM Backend

Django + Django REST Framework starter for the Nugabest CRM.

## Requirements

- Python 3.12–3.14 (Python 3.13 recommended)
- PostgreSQL for shared/integration/production environments
- Git

## Windows PowerShell setup

From the repository root:

```powershell
cd backend
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py check
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/api/v1/health/` to verify the API process.

## macOS / Linux setup

```bash
cd backend
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python manage.py check
python manage.py migrate
python manage.py runserver
```

## PostgreSQL configuration

For PostgreSQL, set these values in `backend/.env`:

```dotenv
DB_ENGINE=django.db.backends.postgresql
DB_NAME=nugabest_crm
DB_USER=nugabest_user
DB_PASSWORD=your-local-password
DB_HOST=127.0.0.1
DB_PORT=5432
DB_SSLMODE=prefer
```

The SQLite setting is only a quick local smoke-test default. PostgreSQL is the agreed project database and must be used for shared development, integration and production.

## Current backend apps

The domain apps are scaffolds only. Their models and migrations will be added after Phase 0 database design approval.
