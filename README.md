# News Application – Django Capstone Project

## Project Overview

The News Application is a role-based content management system built with Django and MariaDB. It enables structured publishing of news articles through an approval workflow.

The system supports multiple user roles:

-  Readers – View approved articles
-  Journalists – Create and manage articles
-  Editors – Review and approve/reject content
-  Admins – Full system control

---

##  Key Features

- Role-Based Authentication & Authorization  
- Article CRUD Operations  
- Editorial Approval Workflow  
- Django Admin Customization  
- MariaDB Database Integration  
- Dockerized Environment (easy setup & deployment)

---

##  Technologies Used

- Python 3.10+
- Django 5.2.11
- MariaDB
- mysqlclient
- Docker & Docker Compose
- HTML5 / CSS3

---

#  Quick Start (Docker - Recommended)

## 1 Run the Project

```bash
docker compose up --build
2️⃣ Apply Migrations (if needed)
docker compose exec web python manage.py migrate
3️⃣ Create Superuser
docker compose exec web python manage.py createsuperuser
4️⃣ Access the App

App: http://localhost:8000

Admin: http://localhost:8000/admin

 Manual Setup (Without Docker)
1️⃣ Clone Repository
git clone <your-repository-url>
cd news_capstone_corrected
2️⃣ Virtual Environment
python -m venv venv

Activate:

Windows:

venv\Scripts\activate

macOS/Linux:

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Setup MariaDB

Install MariaDB: https://mariadb.org/download/

Create database:

CREATE DATABASE news_capstone_db;
5️⃣ Configure Database

Update settings.py:

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
6️⃣ Run Migrations
python manage.py migrate
7️⃣ Run Server
python manage.py runserver
 User Roles & Permissions
 Reader

View approved articles only

 Journalist

Create articles

Edit/Delete own articles

Cannot approve content

 Editor

Approve/Reject articles

Edit/Delete all articles

 Superuser

Full administrative access

 Approval Workflow

Journalist creates article → approved = False

Editor reviews article

Editor approves → approved = True

Article becomes visible to readers

 Test Accounts (Optional)

 For demo purposes only

Reader

Username: reader1

Password: Mojalefa1999

Journalist

Username: journalist1

Password: Mojalefa1999

Editor

Username: editor1

Password: Mojalefa1999

Superuser

Username: Pablo

Password: #Barblo@123

 Project Structure
news_capstone_corrected/
│
├── news/
├── templates/
├── static/
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── requirements.txt
└── README.md
 requirements.txt
Django==5.2.11
mysqlclient==2.2.4
 Development Notes

Uses MariaDB inside Docker container

Default DB port: 3306

Containers:

web → Django app

db → MariaDB

Ensure Docker is running before starting

 Author

Mojalefa Mokati
Email: mokatimojalefa781@gmail.com

 Capstone Submission Statement

This project was developed as part of a Software Engineering Capstone Project.

It demonstrates:

Django backend development

Role-based access control

MariaDB integration

Docker containerization

Real-world editorial workflow system

#  Capstone Submission Statement


