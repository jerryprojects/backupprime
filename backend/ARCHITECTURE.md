# PRIME Backend - Architecture & API Reference

## System Architecture

```
Frontend (React/TypeScript)
         ↓
      [HTTP REST API]
         ↓
Django REST Framework
↓        ↓        ↓        ↓
Models Serializers Views URLs
↓        ↓        ↓        ↓
      SQLite3 Database
```

## Database Schema

### UserProfile
- Extends Django's User model
- Stores role and additional user information
- Created automatically when user is created via signals

### Project
- Main project entity
- Owner: ForeignKey to User
- Approved Faculty: ManyToMany relationship for access control
- Fields: title, abstract, domains, year, license, tech_stack, status

### TeamMember
- Associates users with projects
- Tracks contributions
- Unique constraint on (project, email)

### AccessRequest
- Tracks faculty access requests to locked projects
- Status: pending, granted, rejected
- Unique constraint on (project, requester)

### Notification
- User notifications for various events
- Types: access_request, access_granted, project_updated, etc.

## API Response Format

### Success Response (200):
```json
{
  "id": "proj-1",
  "title": "Project Title",
  "abstract": "Description",
  ...
}
```

### Error Response (4xx/5xx):
```json
{
  "error": "Error message",
  "detail": "Detailed explanation"
}
```

## Authentication Flow

```
Client                  Backend
  │                       │
  ├──POST /auth/token──→  │
  │  {username, password}  │
  │                    (Validate credentials)
  │                       │
  │  ←──Token────────────│
  │                       │
  ├──GET /projects/───→  │
  │  Header: Authorization: Token XXX
  │                       │
  │  ←──Projects List──── │
```

## Role-Based Access Control

### Student:
- Can create and delete own projects
- Can see all public projects
- Cannot modify locked projects

### Faculty:
- Can see all public projects
- Can see projects they have access to
- Can request access to locked projects
- Have own projects

### Admin:
- Can see all projects
- Can approve/reject project creation
- Can access all project data
- Can manage users

## Project Lifecycle

```
Created (status: public)
    ↓
[Owner manages]
    ↓
┌─────────────────────┐
│  Faculty requests   │
│  access (locked)    │
└─────┬───────────────┘
      │
      ├─→ Owner approves ──→ Notification ──→ Approved
      │
      └─→ Owner denies ──→ Notification ──→ Pending
```

## Pagination

List endpoints support pagination:
```
GET /api/projects/?page=1&page_size=20
```

Response:
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/projects/?page=2",
  "previous": null,
  "results": [...]
}
```

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Server Error |

## Performance Optimizations

- Database indexes on frequently queried fields
- Serializer optimization with read_only fields
- Pagination to limit large result sets
- Signal handlers for data consistency

## Security Features

- CSRF protection
- CORS validation
- Token-based authentication
- Permission classes on all views
- SQL injection protection via ORM
- Input validation on serializers

## Available Commands

```bash
# Development
python manage.py runserver
python manage.py shell
python manage.py test

# Database
python manage.py migrate
python manage.py makemigrations

# Data
python manage.py load_sample_data
python manage.py createsuperuser

# Admin
python manage.py collectstatic
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| SECRET_KEY | dev-key | Django secret key |
| DEBUG | True | Debug mode |
| ALLOWED_HOSTS | localhost | Allowed hosts |
| CORS_ALLOWED_ORIGINS | localhost:5173 | CORS origins |
| DATABASE_URL | sqlite3 | Database connection |

## Logging

Logs are printed to console. Configure in `settings.py` LOGGING section.

## API Evolution & Versioning

Current API version: 1.0 (no explicit versioning)
Future: Consider implementing versioning with `/api/v1/` prefix

## Rate Limiting

Not implemented in default setup. For production, add:
```bash
pip install djangorestframework-simplejwt
# or
pip install django-ratelimit
```

## Testing Strategy

- Unit tests for models
- Integration tests for views
- Use Django TestCase for database operations

Run tests:
```bash
python manage.py test api
python manage.py test --verbosity=2
```

## Deployment Checklist

- [ ] Set DEBUG=False
- [ ] Update SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Update CORS_ALLOWED_ORIGINS
- [ ] Use production database (PostgreSQL)
- [ ] Set up HTTPS/SSL
- [ ] Configure static files
- [ ] Set up logging to file
- [ ] Configure backups
- [ ] Set up monitoring
- [ ] Use Gunicorn/uWSGI
- [ ] Configure Nginx reverse proxy
