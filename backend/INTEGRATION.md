# Backend Integration Guide

This document explains how to integrate the Django backend with your React frontend.

## API Base URL

The backend API runs on: `http://localhost:8000/api/`

## Authentication

The API uses Token-based authentication. Steps:

1. Obtain a token by sending credentials to:
   ```
   POST /api/auth/token/
   ```
   
   Example:
   ```javascript
   const response = await fetch('http://localhost:8000/api/auth/token/', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({
       username: 'sarah',
       password: 'testpass123'
     })
   });
   const { token } = await response.json();
   localStorage.setItem('authToken', token);
   ```

2. Include the token in all authenticated requests:
   ```javascript
   const headers = {
     'Authorization': `Token ${localStorage.getItem('authToken')}`,
     'Content-Type': 'application/json'
   };
   ```

## Frontend Configuration

### 1. Create API service file (src/api/client.ts):

```typescript
const API_BASE_URL = 'http://localhost:8000/api';

export const apiClient = async (
  endpoint: string,
  options: RequestInit = {}
) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = localStorage.getItem('authToken');
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (token) {
    headers['Authorization'] = `Token ${token}`;
  }
  
  const response = await fetch(url, {
    ...options,
    headers,
  });
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }
  
  return response.json();
};
```

### 2. Implement Login:

```typescript
export async function login(email: string, password: string) {
  const response = await fetch('http://localhost:8000/api/auth/token/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: email, password })
  });
  
  const { token } = await response.json();
  localStorage.setItem('authToken', token);
  
  // Fetch user profile
  const profile = await apiClient('/profiles/me/');
  return { token, profile };
}
```

### 3. Update Mock Data Calls to API Calls:

Replace:
```typescript
import { mockProjects } from './data/mockData';
const projects = mockProjects;
```

With:
```typescript
const projects = await apiClient('/projects/');
```

## API Endpoints

### Authentication
- `POST /auth/token/` - Get authentication token
- `GET /auth/` - Session authentication endpoints

### Projects
- `GET /projects/` - List all public projects
- `POST /projects/` - Create new project
- `GET /projects/{id}/` - Get project details
- `PUT /projects/{id}/` - Update project
- `DELETE /projects/{id}/` - Delete project
- `GET /projects/my_projects/` - Get user's projects
- `POST /projects/{id}/request_access/` - Request access
- `POST /projects/{id}/approve_access/` - Approve access
- `POST /projects/{id}/deny_access/` - Deny access

### Users
- `GET /users/` - List users
- `GET /users/me/` - Get current user
- `GET /profiles/me/` - Get user profile

### Notifications
- `GET /notifications/` - List notifications
- `POST /notifications/{id}/mark_as_read/` - Mark as read
- `POST /notifications/mark_all_as_read/` - Mark all as read
- `GET /notifications/unread_count/` - Get unread count

### Team Members
- `POST /team-members/` - Add team member
- `DELETE /team-members/{id}/` - Remove team member

### Access Requests
- `GET /access-requests/` - List access requests

## Environment Setup

Create `.env` in the frontend root (if using):

```env
VITE_API_URL=http://localhost:8000/api
```

Then use:
```typescript
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
```

## CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Another dev port)
- `http://127.0.0.1:5173`

If running on a different port, update `CORS_ALLOWED_ORIGINS` in `backend/config/settings.py`.

## Data Models Mapping

The backend models align with your frontend interfaces:

### User (matches current User interface)
```json
{
  "id": 1,
  "username": "sarah",
  "email": "sarah@university.edu",
  "first_name": "Sarah",
  "last_name": "Johnson",
  "profile": {
    "role": "student",
    "bio": "...",
    "department": "..."
  }
}
```

### Project (matches current Project interface)
```json
{
  "id": "proj-1",
  "title": "...",
  "abstract": "...",
  "domains": ["AI", "NLP"],
  "year": "2024-25",
  "license": "MIT",
  "tech_stack": ["Python"],
  "status": "public",
  "owner": { /* User object */ },
  "team_members": [
    {
      "id": "tm-1",
      "name": "...",
      "email": "...",
      "contribution": "..."
    }
  ],
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## Testing the Integration

1. Start the backend:
   ```bash
   python manage.py runserver
   ```

2. Start the frontend:
   ```bash
   npm run dev
   ```

3. Open browser console and test:
   ```javascript
   fetch('http://localhost:8000/api/projects/')
     .then(r => r.json())
     .then(data => console.log(data));
   ```

4. Try logging in through the UI - it should authenticate with the backend

## Deployment

For production deployment:

1. Build frontend:
   ```bash
   npm run build
   ```

2. Serve from backend static files or separate domain with proper CORS

3. Update `API_BASE_URL` to production URL

4. Configure production settings in Django

See [Backend README](README.md) for production deployment details.
