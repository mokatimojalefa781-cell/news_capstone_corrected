# News Application – Django Capstone Project

##  Project Overview

The News Application is a role-based content management system developed using Django and MariaDB as part of a Software Engineering Capstone Project.

The system allows:

- Readers to view approved news articles
- Journalists to create and manage articles
- Editors to review and approve content before publication

The project demonstrates:

- Django Models and ORM
- Role-Based Authentication & Authorization
- CRUD Operations
- Content Approval Workflow
- MariaDB Database Integration
- Admin Panel Customization


---

#  Technologies Used

- Python 3.10+
- Django 5.2.11
- MariaDB
- mysqlclient (MariaDB connector)
- HTML5 / CSS3


---

#  Step-by-Step Installation Guide

Follow these steps carefully to set up the project from scratch.

---

## 1️ Clone the Repository

```bash
git clone <your-repository-url>
cd news_capstone_corrected
```

---

## 2️ Create and Activate Virtual Environment

Create virtual environment:

```bash
python -m venv venv
```

Activate it:

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

---

## 3️ Install Project Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️ Install and Configure MariaDB

### Install MariaDB

Download and install MariaDB from the official website:
https://mariadb.org/download/

During installation:
- Set root password
- Enable TCP/IP
- Keep default port (3306)

---

### Create Database

Login to MariaDB:

```bash
mysql -u root -p
```

Create database:

```sql
CREATE DATABASE news_capstone_db;
```

Create user (recommended):

```sql
CREATE USER 'newsuser'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON news_capstone_db.* TO 'newsuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## 5️ Configure Django to Use MariaDB

In `settings.py`, update the DATABASES section:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'news_capstone_db',
        'USER': 'newsuser',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## 6️ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create all tables inside the MariaDB database.

---

## 7️ Create Superuser

```bash
python manage.py createsuperuser
```

Follow prompts to create admin account.

---

## 8️ Run Development Server

```bash
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000
```

---

# User Roles & Permissions

### Reader
- View approved articles only

### Journalist
- Create new articles
- Edit/Delete their own articles
- Cannot approve content

### Editor
- Approve or reject articles
- Edit/Delete all articles

### Superuser
- Full administrative access

---

# Test Accounts (If Preloaded)

You may use:

Reader:
Username: reader1  
Password: Mojalefa1999  

Journalist:
Username: journalist1  
Password: Mojalefa1999  

Editor:
Username: editor1  
Password: Mojalefa1999  

Superuser:
Username: Pablo  
Password: #Barblo@123  

---

#  Project Structure

```
news_capstone_corrected/
│
├── news/                # Main Django application
├── templates/           # HTML templates
├── static/              # Static files
├── manage.py
├── requirements.txt
└── README.md
```

---

#  requirements.txt

Ensure your `requirements.txt` contains:

```
Django==5.2.11
mysqlclient==2.2.4
```

---

#  Approval Workflow

- Articles are created with `is_approved = False`
- Editors change `is_approved = True`
- Only approved articles are visible to Readers

---

#  Development Notes

- Database: MariaDB
- Default port: 3306
- Ensure MariaDB service is running before starting Django
- Use virtual environment to isolate dependencies

---

#  Contact

Mojalefa Mokati  
Email: mokatimojalefa781@gmail.com  

---

#  Capstone Submission Statement

This project was developed as part of a Software Engineering Capstone.  
It demonstrates backend development using Django, role-based permissions, database integration with MariaDB, and a content approval workflow.
