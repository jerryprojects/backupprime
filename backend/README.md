# Django + SQLite Backend for PRIME Project Hub

This is the Django backend API for the PRIME Project Hub frontend application.

## Features

- **User Authentication**: Token-based authentication with role-based access control (Student, Faculty, Admin)
- **Project Management**: Create, read, update, and delete projects
- **Team Collaboration**: Manage team members and contributions
- **Access Control**: Faculty can request access to locked projects; owners can approve/deny
- **Notifications**: Real-time notifications for access requests, approvals, and project updates
- **Admin Dashboard**: Full admin interface with Django admin

## Technology Stack

- Django 4.2
- Django REST Framework
- SQLite3
- Python 3.8+

## Project Structure

```
backend/
├── config/              # Django project configuration
│   ├── settings.py      # Settings file
│   ├── urls.py          # URL routing
│   ├── wsgi.py          # WSGI application
│   └── asgi.py          # ASGI application
├── api/                 # Main API app
│   ├── models.py        # Database models
│   ├── views.py         # ViewSets and Views
│   ├── serializers.py   # DRF Serializers
│   ├── urls.py          # API URL routing
│   ├── admin.py         # Django admin configuration
│   ├── signals.py       # Django signals
│   └── tests.py         # Tests
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables example
└── db.sqlite3           # SQLite database (auto-generated)
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create .env file:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your configuration (optional for development)

6. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin user.

8. **Load sample data (optional):**
   ```bash
   python manage.py shell
   ```
   Then in the shell:
   ```python
   from django.contrib.auth.models import User
   from api.models import Project, TeamMember
   
   # Create test users
   user1 = User.objects.create_user(username='student1', email='student1@example.com', password='pass123')
   user1.profile.role = 'student'
   user1.profile.save()
   
   user2 = User.objects.create_user(username='faculty1', email='faculty1@example.com', password='pass123')
   user2.profile.role = 'faculty'
   user2.profile.save()
   
   # Create sample project
   project = Project.objects.create(
       title='AI Chatbot Project',
       abstract='An intelligent chatbot for campus support',
       owner=user1,
       year='2024-25',
       status='public'
   )
   exit()
   ```

9. **Run development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Authentication
- `POST /api/auth/token/` - Get authentication token
- `GET /api/auth/` - Session authentication endpoints

### Users
- `GET /api/users/` - List all users
- `POST /api/users/` - Create new user
- `GET /api/users/{id}/` - Get user details
- `GET /api/users/me/` - Get current user profile
- `GET /api/users/{id}/projects/` - Get user's projects

### Projects
- `GET /api/projects/` - List all public projects
- `POST /api/projects/` - Create new project (authenticated)
- `GET /api/projects/{id}/` - Get project details
- `PUT /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project
- `GET /api/projects/my_projects/` - Get user's projects
- `POST /api/projects/{id}/request_access/` - Request access to locked project
- `POST /api/projects/{id}/approve_access/` - Approve access request
- `POST /api/projects/{id}/deny_access/` - Deny access request
- `POST /api/projects/{id}/add_team_member/` - Add team member
- `GET /api/projects/{id}/access_requests/` - Get access requests

### Team Members
- `GET /api/team-members/` - List team members
- `POST /api/team-members/` - Add team member
- `GET /api/team-members/{id}/` - Get team member details
- `DELETE /api/team-members/{id}/` - Remove team member

### Access Requests
- `GET /api/access-requests/` - List access requests
- `GET /api/access-requests/{id}/` - Get access request details

### Notifications
- `GET /api/notifications/` - List user's notifications
- `POST /api/notifications/{id}/mark_as_read/` - Mark notification as read
- `POST /api/notifications/mark_all_as_read/` - Mark all as read
- `GET /api/notifications/unread_count/` - Get unread count

## Authentication

The API uses Token Authentication. To authenticate:

1. Get a token:
   ```bash
   curl -X POST http://localhost:8000/api/auth/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "youruser", "password": "yourpass"}'
   ```

2. Include the token in requests:
   ```bash
   curl -H "Authorization: Token YOUR_TOKEN_HERE" \
     http://localhost:8000/api/projects/
   ```

## Database Models

### UserProfile
- Extended user profile with role information
- Roles: student, faculty, admin

### Project
- Main project model with all project details
- Statuses: public, locked, approved
- Approval statuses: pending, approved, rejected

### TeamMember
- Team members associated with projects

### AccessRequest
- Faculty access requests to locked projects

### Notification
- User notifications for various events

## Admin Interface

Access the Django admin at `http://localhost:8000/admin/` using the superuser credentials you created.

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

## Development

### Run Tests
```bash
python manage.py test
```

### Run with auto-reload
```bash
python manage.py runserver
```

### Create Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Set a strong `SECRET_KEY`
3. Update `ALLOWED_HOSTS` with your domain
4. Use a production database (PostgreSQL recommended)
5. Use a production WSGI server (Gunicorn, uWSGI)
6. Set up proper CORS configuration
7. Use HTTPS

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Connecting Frontend and Backend

The frontend (React app running on port 5173) is configured to communicate with this backend. Make sure:

1. Backend is running on `http://localhost:8000`
2. CORS is properly configured in `settings.py`
3. Frontend API base URL is set correctly

In your React frontend, configure API calls:
```javascript
const API_BASE = 'http://localhost:8000/api';

// Example API call
const response = await fetch(`${API_BASE}/projects/`, {
  headers: { 'Authorization': `Token ${token}` }
});
```

## Troubleshooting

### Database Issues
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### CORS Errors
Ensure frontend URL is in `CORS_ALLOWED_ORIGINS` in settings.py

### Import Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Support

For issues or questions, check the Django and Django REST Framework documentation:
- [Django Documentation](https://docs.djangoproject.com/)
- [DRF Documentation](https://www.django-rest-framework.org/)
