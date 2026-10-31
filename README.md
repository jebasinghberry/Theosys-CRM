# Nugabest Massage Clinic CRM

A multi-centre clinic CRM built with **React + TypeScript** (frontend), **Django + Django REST Framework** (backend), and **PostgreSQL** (database).

## Repository branches

- `main` — integration/release branch. Changes land here through reviewed pull requests.
- `frontend` — React application work.
- `backend` — Django REST API and business logic work.

Create feature branches from the relevant work branch, for example `feature/patient-enrollment` from `backend`.

## Current status

Phase 0 is in progress. This repository contains the project baseline, architecture notes, and a Django backend scaffold. Business models and migrations are deliberately not created until the Phase 0 ER diagram and requirements are approved.

## Project structure

```text
backend/      Django project, REST API and domain apps
frontend/     React application (starter branch)
docs/         Phase 0 decisions, architecture and approval checklists
```

See `backend/README.md` for backend setup and `docs/PHASE_ZERO.md` for the current Phase 0 decisions.
