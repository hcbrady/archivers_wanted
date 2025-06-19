# Archivers Wanted

**Archivers Wanted** is a Django-based web application designed to make it easier to discover and contribute to projects across the Internet Archive. Inspired by research on participation infrastructure and contributor motivation, this tool centralizes open contribution opportunities in one place and makes them filterable by interest and skill set.

## Features

- View a list of current contribution opportunities
- Read detailed summaries for each opportunity
- (PLANNED) Tagging system for filtering by skill and interest
- (PLANNED) GitHub integration for auto-importing "good first issues"
- (PLANNED) Community-submitted opportunities
- (PLANNED) Subscription to skill and interest tags

---

## Tech Stack

- **Framework:** Django (Python)
- **Database:** PostgreSQL
- **Frontend:** Bootstrap
- **Deployment:** Render (planned)

---

## Local Setup

1. **Clone the repository:**

```bash
git clone https://github.com/hcbrady/archivers_wanted.git
cd archivers_wanted
```

2. **Create and activate a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
export DB_PASSWORD='your_postgres_password'
```

5. **Run migrations and start the server:**
```bash
python manage.py migrate
python manage.py runserver
```

6. **Visit: http://127.0.0.1:8000**





