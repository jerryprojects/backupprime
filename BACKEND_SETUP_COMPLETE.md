# PRIME Backend Setup Complete ✅

## 📁 What Was Created

Your Django backend is now ready! Here's what was set up:

### Core Backend Structure
```
backend/
├── config/                    # Django project settings
│   ├── settings.py           # Main configuration
│   ├── settings_production.py # Production overrides
│   ├── urls.py               # URL routing
│   ├── wsgi.py               # WSGI application
│   └── asgi.py               # ASGI application
│
├── api/                       # Main API application
│   ├── models.py             # Database models
│   │  └── UserProfile, Project, TeamMember, AccessRequest, Notification
│   ├── serializers.py        # DRF serializers
│   ├── views.py              # ViewSets & views
│   ├── urls.py               # API routes
│   ├── admin.py              # Admin interface configuration
│   ├── apps.py               # App configuration
│   ├── signals.py            # Django signals
│   ├── tests.py              # Unit tests
│   ├── migrations/           # Database migrations
│   └── management/commands/  # Custom commands
│       └── load_sample_data.py
│
├── manage.py                  # Django management
├── requirements.txt           # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── init_db.py                 # Database initialization script
├── setup_windows.bat          # Windows setup script
├── setup_linux.sh             # Linux/Mac setup script
└── README.md                  # Full documentation
```

### Documentation Files Created
- **README.md** - Complete backend documentation
- **QUICKSTART.md** - 5-minute quick start guide
- **INTEGRATION.md** - How to connect with React frontend
- **ARCHITECTURE.md** - API design & architecture

### Docker Support
- **Dockerfile** - Backend container
- **docker-compose.yml** - Full stack (Backend + Database + Frontend)

### Features Included

✅ **User Management**
- Role-based access control (Student, Faculty, Admin)
- User profiles with extended information
- Automatic profile creation on user signup

✅ **Project Management**
- Create, read, update, delete projects
- Multiple status levels (public, locked, approved)
- Approval workflow for projects

✅ **Collaboration Features**
- Team member management
- Contribution tracking
- Faculty access requests to locked projects

✅ **Integration**
- RESTful API with Django REST Framework
- Token-based authentication
- CORS enabled for frontend
- Comprehensive error handling

✅ **Admin Interface**
- Full Django admin panel
- Manage all entities
- User role assignment
- Approve/deny access requests

## 🚀 Quick Start (2 Minutes)

### Windows:
```powershell
cd backend
.\setup_windows.bat
python manage.py runserver
```

### Mac/Linux:
```bash
cd backend
chmod +x setup_linux.sh
./setup_linux.sh
python manage.py runserver
```

## 📊 Database Models

### UserProfile
- Stores user roles: student, faculty, admin
- Bio, phone, department
- Auto-created with User model

### Project
- Title, abstract, domains, tech stack
- Owner (ForeignKey to User)
- Status: public, locked, approved
- Approval status: pending, approved, rejected
- Approved faculty (ManyToMany)

### TeamMember
- Name, email, contribution
- Associated with project
- Tracks team composition

### AccessRequest
- Faculty requesting access to locked projects
- Status tracking: pending, granted, rejected
- Response management

### Notification
- User notifications
- Multiple types: access_request, access_granted, etc.
- Read/unread tracking

## 🔐 Authentication

Token-based authentication:
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "sarah", "password": "testpass123"}'
```

Include token in requests:
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/projects/
```

## 📱 Sample Users (after load_sample_data)

| Username | Password | Role |
|----------|----------|------|
| sarah | testpass123 | Student |
| mike | testpass123 | Student |
| emma | testpass123 | Student |
| faculty_john | testpass123 | Faculty |
| admin_user | testpass123 | Admin |

## 🔗 Connect Frontend

In your React app, set API base URL:
```javascript
const API_BASE = 'http://localhost:8000/api';

// Authenticate
const res = await fetch(`${API_BASE}/auth/token/`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'sarah', password: 'testpass123' })
});
const { token } = await res.json();

// Use token
const projects = await fetch(`${API_BASE}/projects/`, {
  headers: { 'Authorization': `Token ${token}` }
});
```

## 📚 Main API Endpoints

### Projects
- `GET /api/projects/` - List projects
- `POST /api/projects/` - Create project
- `GET /api/projects/{id}/` - Get details
- `PUT /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project

### Teams
- `POST /api/team-members/` - Add member
- `DELETE /api/team-members/{id}/` - Remove member

### Access Control
- `POST /api/projects/{id}/request_access/` - Request access
- `POST /api/projects/{id}/approve_access/` - Approve access
- `POST /api/projects/{id}/deny_access/` - Deny access

### Notifications
- `GET /api/notifications/` - List notifications
- `POST /api/notifications/{id}/mark_as_read/` - Mark as read
- `GET /api/notifications/unread_count/` - Unread count

## 🐳 Docker Support

Run entire stack with Docker:
```bash
docker-compose up -d
```

This will start:
- Backend (Django) on port 8000
- Frontend (Vite) on port 5173
- Database (PostgreSQL) on port 5432

## 📋 Commands Reference

```bash
# Development
python manage.py runserver           # Start dev server
python manage.py runserver 8001      # Custom port

# Database
python manage.py migrate             # Apply migrations
python manage.py makemigrations      # Create migrations

# Data
python manage.py createsuperuser     # Create admin user
python manage.py load_sample_data    # Load test data
python manage.py shell               # Django shell

# Static files
python manage.py collectstatic       # Collect static files

# Testing
python manage.py test                # Run tests
python manage.py test api            # Test specific app

# Backup
chmod +x backup.sh
./backup.sh                          # Backup database
```

## ⚙️ Configuration

### For Development (default)
- DEBUG = True
- SQLite3 database
- CORS enabled for localhost

### For Production
Update `backend/config/settings_production.py`:
1. Set SECRET_KEY
2. Update ALLOWED_HOSTS
3. Configure database (PostgreSQL recommended)
4. Update CORS_ALLOWED_ORIGINS
5. Enable HTTPS

Then use:
```bash
DJANGO_SETTINGS_MODULE=config.settings_production python manage.py runserver
```

## 🔄 Workflow Examples

### Create a Project
```bash
curl -X POST http://localhost:8000/api/projects/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Project",
    "abstract": "Description",
    "year": "2024-25",
    "domains": ["AI"],
    "tech_stack": ["Python"],
    "license": "MIT"
  }'
```

### Request Access to Locked Project
```bash
curl -X POST http://localhost:8000/api/projects/proj-1/request_access/ \
  -H "Authorization: Token FACULTY_TOKEN"
```

### Approve Access (Project Owner)
```bash
curl -X POST http://localhost:8000/api/projects/proj-1/approve_access/ \
  -H "Authorization: Token OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"faculty_id": 5}'
```

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | `python manage.py runserver 8001` |
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Database errors | `rm db.sqlite3 && python manage.py migrate` |
| CORS errors | Check `CORS_ALLOWED_ORIGINS` in settings.py |
| No permissions | Check user role in admin panel |

## 📖 Documentation Files

Read more in these docs:
- [Full README](README.md) - Complete reference
- [Quick Start](QUICKSTART.md) - Quick setup guide
- [Integration Guide](INTEGRATION.md) - Frontend integration
- [Architecture](ARCHITECTURE.md) - System design

## 🎯 Next Steps

1. ✅ Backend created with Django
2. ✅ SQLite3 database configured
3. ✅ Models and API endpoints ready
4. ✅ Authentication system in place
5. 👉 **Load sample data**: `python manage.py load_sample_data`
6. 👉 **Connect frontend** to API
7. 👉 **Test the integration**
8. 👉 **Deploy to production**

## 📧 Support Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Python Documentation](https://docs.python.org/)

---

🎉 Your Django backend is ready! Start with the QUICKSTART.md guide and read INTEGRATION.md to connect your React frontend.
