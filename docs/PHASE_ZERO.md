# Phase 0 — Requirements, architecture and approval

**Project:** Nugabest Massage Clinic CRM  
**Status:** In progress  
**Baseline:** Nugabest – Insight client requirements and existing Nugabest CRM overview.

## 1. Confirmed technical direction

| Layer | Technology | Notes |
|---|---|---|
| Frontend | React + TypeScript | Modern responsive CRM interface |
| Backend | Django + Django REST Framework | REST API and business rules |
| Database | PostgreSQL | Primary production database |
| Version control | Git + GitHub | `main`, `frontend`, `backend` |

## 2. Confirmed repository branches

- `main`: reviewed integration/release branch.
- `frontend`: React work branch.
- `backend`: Django work branch.

Work should be developed on the relevant branch and merged to `main` through pull requests after review and tests.

## 3. Business modules in the source baseline

- Login, password change/reset and SMS/WhatsApp OTP recovery.
- Staff registration, privilege assignment, staff ID generation and staff ID card.
- Patient enrollment, referral source, team suggestion, patient ID generation and patient ID card.
- Centres, centre managers/incharges, teams, batches and slots.
- Patient and staff attendance, barcode scanning, Sunday/declared holiday rules.
- Demo machine assignment/booking, machine inventory and cost.
- Invoice and EMI receipt workflows.
- Targets, campaigns and demo-opted lists.
- Dashboard, patient/staff referral reports, graphs and audit trail.
- Filtered SMS and WhatsApp messaging.

Existing CRM overview also retains therapy, appointments, payroll, general inventory, notifications, broader reports and branch/team management. Their detailed workflows must be approved before schema freeze.

## 4. User roles

- Facility Owner / MD
- Centre Manager
- Centre Incharge
- Senior Staff / Team Lead
- Junior Staff

The source rules state that a Centre Manager may access multiple assigned centres, each staff member has one centre assignment, Centre Incharge and staff are restricted to assigned centres, and the Super User has all-module access. Final role-permission matrix must be approved before implementation.

## 5. Business rules requiring design coverage

- Staff ID pattern: branch code + `ST` + sequential number (example: `NGLST001`).
- Patient ID pattern: branch code + two-digit year + sequence (example: `NGL260001`).
- Age is calculated from DOB; source requirements specify above 18.
- Aadhaar: 12 digits; mobile: 10 digits; PIN: 6 digits; PAN pattern and need for PIN database validation need client confirmation.
- Patient referral source influences the suggested team; authorized user may change the team.
- Sundays and declared holidays are exempted from the applicable patient attendance sequence.
- ID generation must be concurrency-safe and IDs must not be reused.

## 6. Initial domain/app map (not final database schema)

`accounts`, `centres`, `staff`, `patients`, `attendance`, `machines`, `billing`, `messaging`, `reports`, `audit`, `notifications`, `common`.

No production data models or migrations are included yet. This is intentional: the client/developer approval requirement says the database and screens must be approved before development starts.

## 7. Decisions to close in Phase 0

1. Approve the role/permission matrix and centre/team access boundaries.
2. Approve screen wireframes and navigation.
3. Approve ER diagram, key constraints, retention and sensitive-field handling.
4. Confirm whether Staff ID is the authentication username or a separate login field.
5. Confirm referral count balancing rules and how team capacity is calculated.
6. Confirm attendance correction, leave, holiday and duplicate-scan rules.
7. Confirm invoice numbering, taxes/discounts, payment methods, EMI schedule, refunds and cancellation.
8. Confirm machine booking and cost history rules.
9. Confirm exact SMS and WhatsApp providers, phone-number ownership, templates, opt-in and delivery status requirements.
10. Finalize therapy, appointments, payroll and general inventory scope.
11. Approve deployment topology, backup schedule, RPO/RTO and user/device requirements.

## 8. Approval record

| Artifact | Owner | Status | Approval date |
|---|---|---|---|
| Requirements baseline | Client + Developer | Pending | — |
| UI wireframes | Client | Pending | — |
| ER diagram / data dictionary | Client + Developer | Pending | — |
| API contract | Developer | Pending | — |
| Security/deployment checklist | Developer + Client | Pending | — |
