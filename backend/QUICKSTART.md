# Quick Start Guide for PRIME Backend

## 🚀 Get Started in 5 Minutes

### For Windows Users:

1. Open PowerShell in the `backend` folder

2. Run the setup script:
   ```powershell
   .\setup_windows.bat
   ```

3. Follow the prompts to create a superuser

4. Start the server:
   ```powershell
   venv\Scripts\activate
   python manage.py runserver
   ```

### For macOS/Linux Users:

1. Open Terminal in the `backend` folder

2. Make the script executable and run it:
   ```bash
   chmod +x setup_linux.sh
   ./setup_linux.sh
   ```

3. Follow the prompts to create a superuser

4. Start the server:
   ```bash
   source venv/bin/activate
   python manage.py runserver
   ```

## 📋 After Initial Setup

### Load Sample Data:
```bash
python manage.py load_sample_data
```

### Access the Services:
- **API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/ (use your superuser credentials)

### Get an Authentication Token:
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "sarah", "password": "testpass123"}'
```

## 🔌 API Usage Examples

### List Projects:
```bash
curl http://localhost:8000/api/projects/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Create a Project:
```bash
curl -X POST http://localhost:8000/api/projects/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Project",
    "abstract": "Project description",
    "year": "2024-25",
    "domains": ["AI"],
    "tech_stack": ["Python"],
    "license": "MIT"
  }'
```

### Request Project Access (Faculty):
```bash
curl -X POST http://localhost:8000/api/projects/{project_id}/request_access/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Approve Access Request (Project Owner):
```bash
curl -X POST http://localhost:8000/api/projects/{project_id}/approve_access/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"faculty_id": 5}'
```

## 🔑 Sample User Credentials

After loading sample data:

| Username | Password | Role |
|----------|----------|------|
| sarah | testpass123 | Student |
| mike | testpass123 | Student |
| emma | testpass123 | Student |
| faculty_john | testpass123 | Faculty |
| admin_user | testpass123 | Admin |

## 🧪 Run Tests:
```bash
python manage.py test
```

## 🗑️ Reset Database:
```bash
# Remove the old database
rm db.sqlite3  # on Linux/macOS
del db.sqlite3  # on Windows PowerShell

# Recreate it
python manage.py migrate
python manage.py createsuperuser
```

## 📦 Deactivate Virtual Environment:
```bash
deactivate
```

## 🆘 Troubleshooting

### Port Already in Use:
```bash
python manage.py runserver 8001
```

### Database Locked Error:
Windows sometimes locks SQLite. Try restarting your terminal and deleting `db.sqlite3`

### Module Not Found:
```bash
pip install -r requirements.txt
```

### CORS Errors with Frontend:
Edit `backend/config/settings.py` and add your frontend URL to `CORS_ALLOWED_ORIGINS`

## 📚 API Documentation

Full API documentation available at: [API_DOCS.md](API_DOCS.md)

## 🔗 Connect with Frontend

Point your React frontend to: `http://localhost:8000/api/`

Example in React:
```javascript
const API_BASE = 'http://localhost:8000/api';

// Authenticate
const response = await fetch(`${API_BASE}/auth/token/`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'sarah', password: 'testpass123' })
});
const { token } = await response.json();

// Use token for authenticated requests
const projects = await fetch(`${API_BASE}/projects/`, {
  headers: { 'Authorization': `Token ${token}` }
});
```

---

Need more help? Check the full [README.md](README.md)
