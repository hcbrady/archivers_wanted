# Archivers Wanted

**Archivers Wanted** is a Django-based web application designed to make it easier to discover and contribute to projects across the Internet Archive. Inspired by research on participation infrastructure and contributor motivation, this tool centralizes open contribution opportunities in one place and makes them filterable by interest and skill set.

## Features

- View a list of current contribution opportunities
- Read detailed summaries for each opportunity
- Tagging system for filtering by skill and interest
- GitHub integration for auto-importing Internet Archive repos with open issues
- Subscription to skill, interest, and project tags
- (PLANNED) Community-submitted opportunities

---

## Tech Stack

- **Framework:** Django (Python)
- **Database:** PostgreSQL
- **Frontend:** Bootstrap
- **Deployment:** Render

---

## Local Setup

**1. Clone the repository:**

```bash
git clone https://github.com/hcbrady/archivers_wanted.git
cd archivers_wanted
```

**2. Create and activate a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Start PostgreSQL and create a database and user:**
```bash
brew services start postgresql
psql postgres
```
Then, in the psql shell:
```bash
CREATE DATABASE archivers_db;
CREATE USER archivers_user WITH PASSWORD 'your_password';
ALTER ROLE archivers_user SET client_encoding TO 'utf8';
ALTER ROLE archivers_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE archivers_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE archivers_db TO archivers_user;
\q
```
**5. Set your environment variable:**
```bash
echo "export DB_PASSWORD='your_password'" >> ~/.zshrc
source ~/.zshrc
```
Alternatively, you can set this manually in your shell before each run:
```bash
export DB_PASSWORD='your_password'
```

**6. Run migrations and start the server:**
```bash
python manage.py migrate
python manage.py runserver
```

**7. Visit: http://127.0.0.1:8000**

**8. Seed your database:**
```bash
python manage.py seed_opportunities
```





