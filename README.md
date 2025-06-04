# 🌐 Social Media API

A fully featured backend REST API built with Django and Django REST Framework, designed for a modern social media platform.

---

## 📌 Features

- 👤 User Authentication (JWT)
- 🔐 Role-based Access Control
- 🧾 Posts, Comments, Likes, and Follows
- 📸 Image Upload Support (via Pillow)
- 📊 Interactive API Docs (Swagger via `drf-yasg`)
- 🛠️ Debug Tools (`django-debug-toolbar`)
- 🧪 Modular Structure for Easy Scaling

---

## ⚙️ Tech Stack

| Tool                    | Description                                 |
|-------------------------|---------------------------------------------|
| Django 5.2.1            | Web framework                               |
| Django REST Framework   | API development                             |
| Simple JWT              | JSON Web Token Authentication               |
| drf-yasg                | Swagger/OpenAPI schema generator            |
| Pillow                  | Image handling                              |
| psycopg2-binary         | PostgreSQL database adapter                 |
| django-debug-toolbar    | In-browser debugging panel                  |
| python-dotenv           | Environment variable management             |

---

## 🚀 Getting Started

### 🔁 1. Clone the Repository

```bash
git clone https://github.com/yourusername/social-media-api.git
cd social-media-api
```

### 🐍 2. Create a Virtual Environment

```bash
# Linux/macOS
python3 -m venv env
source env/bin/activate

# Windows
python -m venv env
env\Scripts\activate
```

### 📦 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Setup

Create a `.env` file in the root directory:

```env
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASS=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

---

## 🗃️ Database Setup

### 🔧 Make Migrations

```bash
python manage.py makemigrations role
python manage.py makemigrations user
```

### ⚙️ Apply Migrations

```bash
python manage.py migrate
```

### 📥 Load Initial Data

```bash
python manage.py loaddata app/role/fixtures/roles.json
```

---

## 🧪 Run Development Server

```bash
python manage.py runserver 0.0.0.0:8000
```

Access API:
```
http://localhost:8000/
```

---

## 📚 API Documentation

Swagger/OpenAPI docs available at:

```
http://localhost:8000/swagger/
```

---

## 🧰 Developer Tools

To view debug info in development:

```
http://localhost:8000/__debug__/
```

---

## 🔄 Update Packages

To review and update outdated packages:

```bash
pip-review --local --interactive
```

---

## 📂 Directory Structure

```
social-media-api/
├── app/
│   ├── user/
│   ├── role/
│   └── ...
├── manage.py
├── requirements.txt
├── .env
└── README.md
```

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the MIT License.