# News Capstone Project

A Django-based news management system with role-based access control for readers, journalists, and editors.

## Features

- User registration and authentication
- Role-based dashboards (Reader, Journalist, Editor)
- Article submission and approval workflow
- Newsletter creation and publishing
- Publisher management

## Setup with Virtual Environment

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd news_capstone_corrected
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the database:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application at http://localhost:8000

## Setup with Docker

1. Ensure Docker is installed and running.

2. Build the Docker image:
   ```bash
   docker build -t news-capstone .
   ```

3. Run the container:
   ```bash
   docker run -p 8000:8000 news-capstone
   ```

4. Access the application at http://localhost:8000

## Environment Variables

Create a `.env` file in the project root with the following variables (for production):

- `DJANGO_SECRET_KEY`: A secret key for Django
- `DJANGO_DEBUG`: Set to `false` for production
- `DATABASE_URL`: Database connection string (if using external DB)

## Documentation

The project documentation is available in the `docs/` folder. Open `docs/index.html` in a web browser to view it.

## Project Structure

- `accounts/`: User authentication and management
- `news/`: Core news functionality (articles, newsletters, publishers)
- `news_project/`: Django project settings
- `static/`: Static files (CSS, JS, images)
- `templates/`: HTML templates
- `docs/`: Generated documentation