from pathlib import Path

# =========================
# BASE DIR
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SECURITY
# =========================
SECRET_KEY = 'django-insecure-temp-key-for-school-project'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# =========================
# APPLICATIONS
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'news',
]

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =========================
# URL CONFIG
# =========================
ROOT_URLCONF = 'news_project.urls'

# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# =========================
# WSGI
# =========================
WSGI_APPLICATION = 'news_project.wsgi.application'

# =========================
# DATABASE (SQLite by default)
# =========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Change to 'django.db.backends.mysql' for MariaDB
        'NAME': BASE_DIR / 'db.sqlite3',         # For MariaDB: 'NAME': 'news_db',
        # For MariaDB, also add:
        # 'USER': 'your_db_user',
        # 'PASSWORD': 'your_db_password',
        # 'HOST': 'localhost',
        # 'PORT': '3306',
    }
}

# =========================
# AUTHENTICATION
# =========================
AUTH_USER_MODEL = 'accounts.CustomUser'
AUTH_PASSWORD_VALIDATORS = []

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "article_list"
LOGOUT_REDIRECT_URL = 'home'


# =========================
# STATIC FILES
# =========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# =========================
# DEFAULTS
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
