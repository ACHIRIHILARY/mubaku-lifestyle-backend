
# Mubaku

Mubaku is a Django-based platform for **barbers and beauty professionals**, designed to connect service providers with clients, manage bookings, and handle transactions.  
The project is containerized with **Docker** and uses a **Makefile** to simplify common development and deployment commands.

---

## 🚀 Features

- 🔑 Authentication & user management  
- 💈 Barber/beauty service listings  
- 📅 Booking system with availability management  
- 💳 Escrow-based transaction flow (MTN & Orange Money support)  
- 📩 Notifications system (emails & in-app)  
- 📦 Docker-based setup for easy local development and deployment  
- 🧩 Environment-based configuration with `.env`  

---

## 🛠 Requirements

- [Docker](https://docs.docker.com/get-docker/)  
- [Docker Compose](https://docs.docker.com/compose/)  
- [GNU Make](https://www.gnu.org/software/make/)

---

## ⚙️ Environment Setup

This project uses environment variables for configuration.  
An example file is provided as `.env.example`.

### 1. Copy `.env.example` → `.env`

```bash
cp .env.example .env
````

### 2. Edit `.env` with your local values

Example configuration:

```env
# Django settings
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=mubaku_db
POSTGRES_USER=mubaku_user
POSTGRES_PASSWORD=supersecret
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Other configs
REDIS_URL=redis://redis:6379/0
```

👉 **Never commit your `.env` file** to Git.

---

## 🐳 Running with Docker

The project ships with a **Makefile** to simplify commands.

### Common Commands

| Command                | Description                              |
| ---------------------- | ---------------------------------------- |
| `make build`           | Build the Docker images                  |
| `make up`              | Start containers in the background       |
| `make logs`            | Tail application logs                    |
| `make down`            | Stop and remove containers               |
| `make shell`           | Open a shell inside the Django container |
| `make migrate`         | Run Django migrations                    |
| `make createsuperuser` | Create a Django admin superuser          |
| `make test`            | Run the test suite                       |

### First-Time Setup

```bash
make build
make up
make migrate
make createsuperuser
```

Then visit: [http://localhost:8000](http://localhost:8000)

---

## 🧪 Running Tests

Run all tests with:

```bash
make test
```

---

## 📂 Project Structure

```
.
├── app
│   ├── apps (project appst, payments, services, bookings, etc...)
│   ├── db.sqlite3
│   ├── manage.py
│   └── mubaku
│       ├── asgi.py
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-310.pyc
│       │   ├── settings.cpython-310.pyc
│       │   ├── urls.cpython-310.pyc
│       │   └── wsgi.cpython-310.pyc
│       ├── settings (project settings at multiple environments)
│       │   ├── base.py
│       │   ├── dev.py
│       │   ├── __init__.py
│       │   ├── prod.py
│       │   └── __pycache__
│       │       ├── base.cpython-310.pyc
│       │       ├── dev.cpython-310.pyc
│       │       └── __init__.cpython-310.pyc
│       ├── urls.py
│       └── wsgi.py
├── docker
│   └── local
│       ├── django
│       │   ├── celery
│       │   │   ├── flower
│       │   │   │   └── start
│       │   │   └── worker
│       │   │       └── start
│       │   ├── Dockerfile
│       │   ├── entrypoint
│       │   └── start
│       └── nginx
│           ├── default.conf
│           └── Dockerfile
├── docker-compose.yml
├── docs
│   └── database
│       ├── database.sql
│       └── seed.sql
├── file.txt
├── makefile
├── mediafiles
├── README.md
├── requirements.txt
├── staticfiles
```
---

## 🤝 Contributing

We welcome contributions! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for details.

---

## 📜 License

This project is licensed under the **MIT License**.


