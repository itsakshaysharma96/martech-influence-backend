# 🚀 Martech Influence Backend - Complete Setup Guide

A comprehensive Django REST Framework backend with Blog, Case Study, Career, Contact, Social Media, and Services management.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Virtual Environment Setup](#virtual-environment-setup)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Installation & Running](#installation--running)
7. [API Documentation (Swagger)](#api-documentation-swagger)
8. [Available APIs](#available-apis)
9. [Project Structure](#project-structure)
10. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (Python 3.12 recommended)
- **pip** (Python package manager)
- **Git** (optional, for version control)

Check your Python version:
```bash
python3 --version
```

---

## 🏃 Quick Start

### Step 1: Navigate to Project Directory
```bash
cd /home/riyazul/Desktop/projects/martech_influence_backend
```

### Step 2: Activate Virtual Environment
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py migrate
```

### Step 5: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Run Development Server
```bash
python manage.py runserver
```

**🎉 Server is now running at:** `http://127.0.0.1:8000/`

---

## 🐍 Virtual Environment Setup

### Create Virtual Environment (if not already created)

**Linux/Mac:**
```bash
python3 -m venv venv
```

**Windows:**
```bash
python -m venv venv
```

### Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Deactivate Virtual Environment
```bash
deactivate
```

---

## ⚙️ Environment Configuration

### Location
The `.env` file is located **outside** the project directory at:
```
/home/riyazul/Desktop/projects/.env
```

### Required Variables

The `.env` file contains all configuration. Here's what you need:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=0.0.0.0,localhost,127.0.0.1

# Database Configuration
DATABASE_URL=sqlite:///db.sqlite3

# Internationalization
LANGUAGE_CODE=en-us
TIME_ZONE=UTC
```

### Database Configuration Options

#### SQLite (Default - No setup required)
```env
DATABASE_URL=sqlite:///db.sqlite3
```

#### PostgreSQL
```env
DATABASE_URL=psql://username:password@127.0.0.1:5432/database_name
```

#### MySQL
```env
DATABASE_URL=mysql://username:password@127.0.0.1:3306/database_name
```

**Note:** For PostgreSQL/MySQL, you need to install the database adapter:
```bash
# PostgreSQL
pip install psycopg2-binary

# MySQL
pip install mysqlclient
```

---

## 💾 Database Setup

### Run Migrations
```bash
python manage.py migrate
```

This creates all necessary database tables.

### Create Superuser (Admin Access)
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

### Access Admin Panel
- URL: `http://127.0.0.1:8000/admin/`
- Use the superuser credentials you just created

---

## 📦 Installation & Running

### Complete Setup Process

1. **Activate Virtual Environment**
   ```bash
   cd /home/riyazul/Desktop/projects/martech_influence_backend
   source venv/bin/activate
   ```

2. **Install/Update Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create Superuser** (First time only)
   ```bash
   python manage.py createsuperuser
   ```

5. **Run Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**
   - Admin Panel: `http://127.0.0.1:8000/admin/`
   - API Docs (Swagger): `http://127.0.0.1:8000/swagger/`
   - API Docs (ReDoc): `http://127.0.0.1:8000/redoc/`

### Run on Custom Port
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 📚 API Documentation (Swagger)

### Access Swagger UI

The project includes **Swagger/OpenAPI** documentation for all APIs.

**Swagger UI (Interactive):**
```
http://127.0.0.1:8000/swagger/
```
or
```
http://127.0.0.1:8000/api-docs/
```

**ReDoc (Alternative UI):**
```
http://127.0.0.1:8000/redoc/
```

**OpenAPI Schema (JSON):**
```
http://127.0.0.1:8000/swagger.json
```

**OpenAPI Schema (YAML):**
```
http://127.0.0.1:8000/swagger.yaml
```

### Features
- ✅ Interactive API testing
- ✅ Request/Response examples
- ✅ Schema definitions
- ✅ Try it out functionality
- ✅ All endpoints documented

---

## 🔌 Available APIs

### Base URL
```
http://127.0.0.1:8000/api/
```

### API Endpoints

#### 📝 Blog APIs
- `GET /api/blog/blogs/` - List all published blogs
- `GET /api/blog/blogs/<id>/` - Get blog details
- `POST /api/blog/blog-leads/` - Submit blog lead

**Query Parameters:**
- `?category=slug` - Filter by category
- `?tag=slug` - Filter by tag
- `?is_featured=true` - Filter featured blogs
- `?search=keyword` - Search blogs
- `?ordering=-created_at` - Order results

#### 📊 Case Study APIs
- `GET /api/casestudy/case-studies/` - List all published case studies
- `GET /api/casestudy/case-studies/<id>/` - Get case study details
- `POST /api/casestudy/case-study-leads/` - Submit case study lead

**Query Parameters:**
- `?category=slug` - Filter by category
- `?industry=name` - Filter by industry
- `?is_featured=true` - Filter featured case studies
- `?search=keyword` - Search case studies

#### 💼 Career APIs
- `GET /api/career/job-postings/` - List all published job postings
- `GET /api/career/job-postings/<id>/` - Get job posting details
- `POST /api/career/job-applications/` - Submit job application

**Query Parameters:**
- `?department=slug` - Filter by department
- `?category=slug` - Filter by category
- `?location=slug` - Filter by location
- `?job_type=slug` - Filter by job type
- `?search=keyword` - Search jobs

#### 📧 Contact APIs
- `POST /api/contact/contacts/` - Submit contact form

#### 🔗 Social Media APIs
- `GET /api/social-media/social-media/` - List all active social media links
- `GET /api/social-media/social-media/<id>/` - Get social media link details

**Query Parameters:**
- `?platform=name` - Filter by platform

#### 🛠️ Services APIs
- `GET /api/services/services/` - List all published services
- `GET /api/services/services/<id>/` - Get service details
- `POST /api/services/service-leads/` - Submit service inquiry

**Query Parameters:**
- `?category=slug` - Filter by category
- `?is_featured=true` - Filter featured services
- `?is_popular=true` - Filter popular services
- `?is_free=true` - Filter free services
- `?search=keyword` - Search services

### Response Format

All APIs return a standardized response:

```json
{
    "status": true,
    "status_code": 200,
    "message_code": "SUCCESS",
    "message": "Operation Successful",
    "data": {
        // Response data here
    },
    "count": 10,
    "next": "http://api.example.com/api/endpoint/?page=2",
    "previous": null
}
```

### Pagination

All list endpoints support pagination:
- Default: 20 items per page
- Use `?page=2` to navigate pages

---

## 📁 Project Structure

```
martech_influence_backend/
├── martech_influence_backend/     # Main project directory
│   ├── settings.py                # Django settings (uses .env)
│   ├── urls.py                    # Main URL configuration
│   └── wsgi.py                    # WSGI configuration
├── blog/                          # Blog app
│   ├── models.py                  # Blog, Category, Tag, BlogLeads
│   ├── views.py                   # API views
│   ├── serializers.py            # API serializers
│   ├── admin.py                  # Admin configuration
│   └── urls.py                   # Blog URLs
├── casestudy/                     # Case Study app
├── career/                        # Career app
├── contact/                        # Contact app
├── socialmedia/                   # Social Media app
├── services/                      # Services app
├── venv/                          # Virtual environment
├── media/                         # User uploaded files
├── staticfiles/                   # Collected static files
├── db.sqlite3                     # SQLite database (if using SQLite)
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
└── README_SETUP.md               # This file
```

**Environment File:**
```
/home/riyazul/Desktop/projects/.env  # Outside project directory
```

---

## 🔧 Troubleshooting

### Issue: Module not found
**Solution:** Activate virtual environment and install requirements
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Database errors
**Solution:** Run migrations
```bash
python manage.py migrate
```

### Issue: .env file not found
**Solution:** Check if `.env` exists at `/home/riyazul/Desktop/projects/.env`

### Issue: Port already in use
**Solution:** Use a different port
```bash
python manage.py runserver 8001
```

### Issue: Static files not loading
**Solution:** Collect static files
```bash
python manage.py collectstatic
```

### Issue: Media files not accessible
**Solution:** Ensure `DEBUG=True` in `.env` file for development

### Issue: Swagger not loading
**Solution:** 
1. Ensure `drf-yasg` is installed: `pip install drf-yasg`
2. Check if `drf_yasg` is in `INSTALLED_APPS`
3. Restart the development server

---

## 📝 Common Commands

### Django Management Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Collect static files
python manage.py collectstatic

# Check for issues
python manage.py check

# Django shell
python manage.py shell
```

### Virtual Environment Commands

```bash
# Activate
source venv/bin/activate

# Deactivate
deactivate

# Install package
pip install package-name

# Install from requirements
pip install -r requirements.txt

# List installed packages
pip list

# Freeze requirements
pip freeze > requirements.txt
```

---

## 🔐 Security Notes

1. **Never commit `.env` file** to version control
2. **Change SECRET_KEY** in production
3. **Set DEBUG=False** in production
4. **Use strong database passwords** in production
5. **Configure ALLOWED_HOSTS** properly for production

---

## 📞 Support

For issues or questions:
- Check the Swagger documentation: `http://127.0.0.1:8000/swagger/`
- Review Django logs in terminal
- Check `.env` file configuration

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Activate venv | `source venv/bin/activate` |
| Install deps | `pip install -r requirements.txt` |
| Run migrations | `python manage.py migrate` |
| Run server | `python manage.py runserver` |
| Access admin | `http://127.0.0.1:8000/admin/` |
| Access Swagger | `http://127.0.0.1:8000/swagger/` |

---

**Happy Coding! 🚀**
