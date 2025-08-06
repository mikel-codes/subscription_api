

---

# **Subscription API Based on Flask and SQLite DB**

# **protip: you can configure this to use any db of your choice**

A **Flask-based REST API** for managing users, subscription plans, and user subscriptions with upgrade/cancel functionality.
Optimized with **SQLAlchemy + raw SQL for performance** and **Alembic migrations** for database schema management.

---

## **Features**

* **User registration & authentication**
* **Subscription plans management** (Free, Pro, etc.)
* **User subscriptions**: subscribe, upgrade, cancel
* **Query optimizations** with raw SQL + indexes
* **Alembic migrations** for schema management
* **Test suite with Pytest**

---

## **1Installation (Local)**

### **Prerequisites**

* Python 3.12+
* SQLite (for local) or MySQL/MariaDB (optional)
* Virtual environment (recommended)

### **Clone the Repository**

```bash
git clone https://github.com/mikel-codes/subscription_api.git
cd subscription_api
```

### **Create and Activate Virtual Environment**

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### **Install Dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ** Database Setup**

### **Configuration**

* Local SQLite (default): `sqlite://subscriptions.db`
* MySQL Example:

  ```bash
  export SQLALCHEMY_DATABASE_URI="mysql+pymysql://user:password@localhost:3306/subscription_db"
  ```

### **Initialize Database**

```bash
flask db init      # only first time
flask db migrate -m "Initial migration"
flask db upgrade
```

*(For quick local dev, you can also use `db.create_all()` in `app.py`.)*

---

## ** Run the Application**

```bash
flask run
```

* API will be available at: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## **Running Tests**

```bash
pytest -v
```

---

## **Running with Docker**

### **Build and Run**

```bash
docker-compose up --build
```

* App runs on: **[http://localhost:5000](http://localhost:5000)**

### **Common Commands**

```bash
# Run migrations inside the container
docker-compose exec web flask db upgrade

# Run tests in the container
docker-compose exec web pytest -v
```

---

## **Example API Endpoints**

| Method | Endpoint                      | Description               |
| ------ | ----------------------------- | ------------------------- |
| POST   | `/auth/register`              | Register a new user       |
| POST   | `/auth/login`                 | Authenticate user         |
| GET    | `/plans/`                     | List subscription plans   |
| POST   | `/plans/`                     | Create a subscription plan|
| POST   | `/subscriptions/subscribe`    | Subscribe to a plan       |
| PUT    | `/subscriptions/<id>/upgrade` | Upgrade user subscription |
| DELETE | `/subscriptions/<id>/cancel`  | Cancel subscription       |
| GET    | `/subscriptions/`             | List all subscriptions    |

**where <id> is user.id**
---

## **7 Project Structure**

```
subscription_api/
│── app.py                # Flask entry point
│── db.py                 # SQLAlchemy & DB setup
│── models.py             # User, Plan, Subscription models
│── routes/
│   ├── auth.py           # Auth endpoints
│   ├── plans.py          # Plan endpoints
│   └── subscription.py   # Subscription endpoints
│── tests/                # Pytest test suite
│── requirements.txt
│── Dockerfile
│── docker-compose.yml
│── README.md
└── instance/             # SQLite DB for dev (gitignored)
```

---

## **Notes**

* Use **`Status` Enum** for subscription statuses to avoid string typos.
* All raw SQL queries are **parameterized** to prevent SQL injection.
* **Active subscription query is indexed** for efficiency.

---
