# API Endpoints Reference

Complete list of all available API endpoints for PRIME Backend.

## Base URL
```
http://localhost:8000/api
```

## Authentication
```
POST /auth/token/
```
Get authentication token using credentials.

**Request:**
```json
{
  "username": "sarah",
  "password": "testpass123"
}
```

**Response:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbea2......"
}
```

---

## Users

### List Users
```
GET /users/
```
Get list of all users.

### Get User Details
```
GET /users/{id}/
```
Get specific user details by ID.

### Get Current User
```
GET /users/me/
```
Get current logged-in user information. (Requires authentication)

### Get User's Projects
```
GET /users/{id}/projects/
```
Get all projects created by a specific user.

### Get User Profile
```
GET /profiles/me/
```
Get current user's profile. (Requires authentication)

---

## Projects

### List All Projects
```
GET /projects/
```
List public projects (or all for authenticated users based on role).

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20)

**Response:**
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/projects/?page=2",
  "previous": null,
  "results": [
    {
      "id": "proj-1",
      "title": "AI Chatbot",
      "abstract": "...",
      "domains": ["AI", "NLP"],
      "year": "2024-25",
      "license": "MIT",
      "tech_stack": ["Python"],
      "status": "public",
      "owner": {...},
      "team_members": [...],
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Create Project
```
POST /projects/
```
Create a new project. (Requires authentication)

**Request:**
```json
{
  "title": "My New Project",
  "abstract": "Project description",
  "domains": ["AI", "Machine Learning"],
  "year": "2024-25",
  "license": "MIT",
  "tech_stack": ["Python", "TensorFlow"],
  "status": "public"
}
```

### Get Project Details
```
GET /projects/{id}/
```
Get detailed information about a project.

### Update Project
```
PUT /projects/{id}/
PATCH /projects/{id}/
```
Update a project. (Requires owner authentication)

### Delete Project
```
DELETE /projects/{id}/
```
Delete a project. (Requires owner authentication)

### Get User's Projects
```
GET /projects/my_projects/
```
Get all projects created by current user. (Requires authentication)

### Request Access
```
POST /projects/{id}/request_access/
```
Request access to a locked project. (Faculty only, requires authentication)

**Response:**
```json
{
  "id": "ar-1",
  "project": "proj-1",
  "requester": {...},
  "status": "pending",
  "requested_at": "2024-01-01T00:00:00Z"
}
```

### Approve Access
```
POST /projects/{id}/approve_access/
```
Approve access request for a faculty member. (Project owner only, requires authentication)

**Request:**
```json
{
  "faculty_id": 5
}
```

### Deny Access
```
POST /projects/{id}/deny_access/
```
Deny access request. (Project owner only, requires authentication)

**Request:**
```json
{
  "faculty_id": 5,
  "message": "Optional denial reason"
}
```

### Add Team Member
```
POST /projects/{id}/add_team_member/
```
Add a team member to a project. (Project owner only, requires authentication)

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "contribution": "Backend Development"
}
```

### Get Access Requests
```
GET /projects/{id}/access_requests/
```
Get all access requests for a project. (Project owner only, requires authentication)

---

## Team Members

### List Team Members
```
GET /team-members/
```
List all team members. (Optional query: `?project={project_id}`)

### Add Team Member
```
POST /team-members/
```
Add a new team member. (Requires authentication)

**Request:**
```json
{
  "project": "proj-1",
  "name": "Jane Smith",
  "email": "jane@example.com",
  "contribution": "Frontend Development"
}
```

### Get Team Member Details
```
GET /team-members/{id}/
```
Get specific team member information.

### Remove Team Member
```
DELETE /team-members/{id}/
```
Remove a team member from a project. (Project owner only, requires authentication)

---

## Access Requests

### List Access Requests
```
GET /access-requests/
```
List access requests for user (both requested and received). (Requires authentication)

**Response:**
```json
[
  {
    "id": "ar-1",
    "project": "proj-1",
    "requester": {
      "id": 5,
      "username": "faculty_john",
      "email": "john@example.com"
    },
    "status": "pending",
    "requested_at": "2024-01-01T00:00:00Z",
    "responded_at": null,
    "response_message": ""
  }
]
```

### Get Access Request Details
```
GET /access-requests/{id}/
```
Get specific access request details. (Requires authentication)

---

## Notifications

### List Notifications
```
GET /notifications/
```
List all notifications for current user. (Requires authentication)

**Response:**
```json
[
  {
    "id": "notif-1",
    "notification_type": "access_granted",
    "title": "Access Granted",
    "message": "Your access request has been approved!",
    "related_project": "proj-1",
    "related_project_title": "AI Chatbot",
    "is_read": false,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Mark as Read
```
POST /notifications/{id}/mark_as_read/
```
Mark a specific notification as read. (Requires authentication)

### Mark All as Read
```
POST /notifications/mark_all_as_read/
```
Mark all notifications as read for current user. (Requires authentication)

### Get Unread Count
```
GET /notifications/unread_count/
```
Get count of unread notifications. (Requires authentication)

**Response:**
```json
{
  "unread_count": 3
}
```

---

## User Profiles

### Get Current Profile
```
GET /profiles/me/
```
Get current user's profile. (Requires authentication)

**Response:**
```json
{
  "role": "student",
  "bio": "Computer Science student",
  "phone": "+1234567890",
  "department": "Computer Science",
  "email": "sarah@university.edu",
  "name": "Sarah Johnson"
}
```

---

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Successful but no content to return |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Permission denied |
| 404 | Not Found - Resource not found |
| 500 | Server Error - Internal server error |

## Error Response Format

```json
{
  "error": "Error message",
  "details": [
    {
      "field": "title",
      "message": "This field is required"
    }
  ]
}
```

## Pagination

List endpoints support pagination:

```
GET /projects/?page=1&page_size=20
```

**Response:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/projects/?page=2",
  "previous": null,
  "results": [...]
}
```

## Status Codes for Projects

| Status | Description |
|--------|-------------|
| public | Visible to all users |
| locked | Only owner and approved faculty can view |
| approved | Admin approved project |

## Approval Statuses

| Status | Description |
|--------|-------------|
| pending | Awaiting admin approval |
| approved | Approved by admin |
| rejected | Rejected by admin |

## Access Request Statuses

| Status | Description |
|--------|-------------|
| pending | Awaiting owner response |
| granted | Access approved by owner |
| rejected | Access denied by owner |

## Notification Types

| Type | Description |
|------|-------------|
| access_request | Someone requested access |
| access_granted | Access was granted |
| project_updated | Project was updated |
| team_member_added | Team member was added |
| admin_message | Message from admin |

## User Roles

| Role | Permissions |
|------|-------------|
| student | Create projects, view public projects |
| faculty | View public & approved projects, request access |
| admin | Full access to all resources |

---

## Example Workflows

### 1. Student Creates Project
```bash
# 1. Authenticate
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "sarah", "password": "testpass123"}'

# 2. Get token from response, then create project
curl -X POST http://localhost:8000/api/projects/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Project",
    "abstract": "Description",
    "domains": ["AI"],
    "year": "2024-25",
    "tech_stack": ["Python"],
    "license": "MIT"
  }'
```

### 2. Faculty Requests Access
```bash
# Get token for faculty user
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "faculty_john", "password": "testpass123"}'

# Request access to locked project
curl -X POST http://localhost:8000/api/projects/proj-1/request_access/ \
  -H "Authorization: Token FACULTY_TOKEN"
```

### 3. Owner Approves Access
```bash
# Get student owner token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "sarah", "password": "testpass123"}'

# Approve access
curl -X POST http://localhost:8000/api/projects/proj-1/approve_access/ \
  -H "Authorization: Token OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"faculty_id": 4}'
```

---

For more information, see the main [README.md](README.md) or [INTEGRATION.md](INTEGRATION.md).
