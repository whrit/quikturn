# Quikturn - Logo Management Platform

Quikturn is a logo management platform that stores and organizes company logos. It provides a RESTful API for managing company information and logos, with integration to an external logo scraper service.

## Features

- Store and manage company information
- Upload and manage company logos
- Automatic logo updates via logo scraper integration
- AWS S3 storage for logo files
- Redis caching for improved performance

## Requirements

- Python 3.12+
- PostgreSQL
- Redis
- AWS S3 bucket
- Logo scraper service

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/quikturn.git
cd quikturn
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a .env file with your configuration:
```bash
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=quikturn
DB_USER=quikturn_user
DB_PASSWORD=your-db-password
DB_HOST=your-rds-endpoint
DB_PORT=5432

# AWS
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=quikturn-logos
AWS_S3_REGION_NAME=us-east-1

# Redis
REDIS_URL=redis://localhost:6379/0
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

- `GET /api/companies/` - List all companies
- `POST /api/companies/` - Create a new company
- `GET /api/companies/{id}/` - Get company details
- `PUT /api/companies/{id}/` - Update company details
- `DELETE /api/companies/{id}/` - Delete a company
- `GET /api/logos/` - List all logos
- `POST /api/logos/` - Upload a new logo
- `GET /api/logos/{id}/` - Get logo details
- `PUT /api/logos/{id}/` - Update logo details
- `DELETE /api/logos/{id}/` - Delete a logo
- `POST /api/logos/{id}/set_primary/` - Set a logo as primary

## Logo Scraper Integration

To update logos using the logo scraper service:

```bash
# Update all companies
python manage.py update_logos

# Update a specific company
python manage.py update_logos --company example.com
```

## Deployment

1. Build the Docker image:
```bash
docker build -t quikturn .
```

2. Run the container:
```bash
docker run -d -p 8000:8000 --env-file .env quikturn
```

## License

MIT License