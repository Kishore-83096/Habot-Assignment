# Employee Management API

## Introduction

This API provides **comprehensive CRUD operations for Employee Management**. Built with **Django REST Framework** and secured using **JWT Authentication**, it enables secure, scalable management of employee data.

### Purpose
- Create, retrieve, update, and delete employees
- Manage employee data efficiently with filtering and pagination
- Ensure secure access through JWT-based authentication

---

## Authentication

### Obtaining a Token

**Endpoint:** `POST /api/token/`

**Request Body:**
```json
{
  "username": "testuser",
  "password": "Test@123"
}
```

**Response Example (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Response (401 Unauthorized):**
```json
{
  "success": false,
  "message": "Invalid credentials"
}
```

### Using Token in Postman

1. **Copy the `access` token** from the response
2. Go to **Postman → Authorization tab**
3. Select **Type:** `Bearer Token`
4. Paste the token in the **Token field**
5. All subsequent requests will include this token in the `Authorization: Bearer <token>` header

> **Important:** Tokens expire after a set period. Use the refresh endpoint below to obtain a new access token without re-authenticating.

### Refreshing Token

**Endpoint:** `POST /api/token/refresh/`

**Request Body:**
```json
{
  "refresh": "refresh_token_from_obtain_response"
}
```

**Response Example (200 OK):**
```json
{
  "success": true,
  "message": "Access token refreshed",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "message": "Invalid refresh token"
}
```

**Error Response (400 Bad Request - Missing Token):**
```json
{
  "success": false,
  "message": "Refresh token required"
}
```

---

## Endpoint Demonstrations

### 1. Create Employee
**Endpoint:** `POST /api/employees/create/`  
**Authentication:** Required (Bearer Token)

#### Success Case: Valid Employee Data

**Request Body:**
```json
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "department": "HR",
  "role": "Manager"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Employee created successfully",
  "data": {
    "id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "department": "HR",
    "role": "Manager",
    "date_joined": "2026-01-14"
  }
}
```

#### Error Case: Duplicate Email (400 Bad Request)

**Request Body:**
```json
{
  "name": "Bob Smith",
  "email": "alice@example.com",
  "department": "Finance",
  "role": "Analyst"
}
```

**Response (400 Bad Request):**
```json
{
  "success": false,
  "message": "Validation error",
  "errors": {
    "email": [
      "employee with this email already exists."
    ]
  }
}
```

#### Error Case: Missing Required Field (400 Bad Request)

**Request Body:**
```json
{
  "email": "charlie@example.com",
  "department": "IT"
}
```

**Response (400 Bad Request):**
```json
{
  "success": false,
  "message": "Validation error",
  "errors": {
    "name": [
      "This field may not be blank."
    ]
  }
}
```

---

### 2. List Employees
**Endpoint:** `GET /api/employees/`  
**Authentication:** Required (Bearer Token)

#### Show All Employees with Pagination

**URL:** `http://127.0.0.1:8000/api/employees/?page=1`

**Response (200 OK):**
```json
{
  "count": 10,
  "next": "http://127.0.0.1:8000/api/employees/?page=2",
  "previous": null,
  "success": true,
  "status_code": 200,
  "message": "Employees retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "Alice Johnson",
      "email": "alice@example.com",
      "department": "HR",
      "role": "Manager",
      "date_joined": "2026-01-14"
    },
    {
      "id": 2,
      "name": "Bob Smith",
      "email": "bob@example.com",
      "department": "Finance",
      "role": "Analyst",
      "date_joined": "2026-01-14"
    },
    {
      "id": 3,
      "name": "Carol White",
      "email": "carol@example.com",
      "department": "IT",
      "role": "Developer",
      "date_joined": "2026-01-14"
    }
  ]
}
```

#### Filter by Department

**URL:** `http://127.0.0.1:8000/api/employees/?department=HR`

**Response (200 OK):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "success": true,
  "status_code": 200,
  "message": "Employees retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "Alice Johnson",
      "email": "alice@example.com",
      "department": "HR",
      "role": "Manager",
      "date_joined": "2026-01-14"
    },
    {
      "id": 4,
      "name": "Diana Prince",
      "email": "diana@example.com",
      "department": "HR",
      "role": "Recruiter",
      "date_joined": "2026-01-14"
    }
  ]
}
```

#### Filter by Role

**URL:** `http://127.0.0.1:8000/api/employees/?role=Manager`

**Response (200 OK):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "success": true,
  "status_code": 200,
  "message": "Employees retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "Alice Johnson",
      "email": "alice@example.com",
      "department": "HR",
      "role": "Manager",
      "date_joined": "2026-01-14"
    }
  ]
}
```

#### No Results - Filter with No Matches

**URL:** `http://127.0.0.1:8000/api/employees/?department=NonExistent`

**Response (200 OK):**
```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "success": true,
  "status_code": 200,
  "message": "Employees retrieved successfully",
  "data": []
}
```

---

### 3. Retrieve Employee
**Endpoint:** `GET /api/employees/{id}/`  
**Authentication:** Required (Bearer Token)

#### Success Case: Employee Found

**Request:** `GET http://127.0.0.1:8000/api/employees/1/`

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Employee retrieved successfully",
  "data": {
    "id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "department": "HR",
    "role": "Manager",
    "date_joined": "2026-01-14"
  }
}
```

#### Error Case: Employee Not Found

**Request:** `GET http://127.0.0.1:8000/api/employees/999/`

**Response (404 Not Found):**
```json
{
  "success": false,
  "message": "Employee not found"
}
```

#### Error Case: Invalid ID Format

**Request:** `GET http://127.0.0.1:8000/api/employees/abc/`

**Response (404 Not Found):**
```json
{
  "success": false,
  "message": "Employee not found"
}
```

---

### 4. Update Employee
**Endpoint:** `PUT /api/employees/{id}/update/`  
**Authentication:** Required (Bearer Token)

#### Modify Employee Details (Full Update)

**Request Body:** (Update department and role)
```json
{
  "department": "Finance",
  "role": "Senior Manager"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Employee updated successfully",
  "data": {
    "id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "department": "Finance",
    "role": "Senior Manager",
    "date_joined": "2026-01-14"
  }
}
```

#### Error Case: Employee Not Found

**Request:** `PUT http://127.0.0.1:8000/api/employees/999/update/`

**Request Body:**
```json
{
  "role": "Director"
}
```

**Response (404 Not Found):**
```json
{
  "success": false,
  "message": "Employee not found"
}
```

#### Error Case: Invalid Email (Duplicate)

**Request Body:**
```json
{
  "email": "bob@example.com"
}
```

**Response (400 Bad Request):**
```json
{
  "success": false,
  "message": "Validation error",
  "errors": {
    "email": [
      "employee with this email already exists."
    ]
  }
}
```

---

### 5. Delete Employee
**Endpoint:** `DELETE /api/employees/{id}/delete/`  
**Authentication:** Required (Bearer Token)

#### Successful Deletion

**Request:** `DELETE http://127.0.0.1:8000/api/employees/1/delete/`

**Response (200 OK):**
```json
{
  "success": true,
  "status_code": 200,
  "message": "Employee deleted successfully",
  "deleted_employee": {
    "id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com"
  }
}
```

#### Error Case: Employee Not Found

**Request:** `DELETE http://127.0.0.1:8000/api/employees/999/delete/`

**Response (404 Not Found):**
```json
{
  "success": false,
  "status_code": 404,
  "message": "Employee not found"
}
```

---

## Quick Start

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser (for admin access)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Running Tests
```bash
python manage.py test api
```

---

## Testing with cURL

### Get Token
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"Test@123"}'
```

### Create Employee (with token)
```bash
curl -X POST http://127.0.0.1:8000/api/employees/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
    "name": "Alice",
    "email": "alice@test.com",
    "department": "HR",
    "role": "Manager"
  }'
```

### List Employees
```bash
curl -X GET http://127.0.0.1:8000/api/employees/ \
  -H "Authorization: Bearer <your_access_token>"
```

### Get Employee by ID
```bash
curl -X GET http://127.0.0.1:8000/api/employees/1/ \
  -H "Authorization: Bearer <your_access_token>"
```

### Update Employee
```bash
curl -X PUT http://127.0.0.1:8000/api/employees/1/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{"department":"Finance","role":"Senior Manager"}'
```

### Delete Employee
```bash
curl -X DELETE http://127.0.0.1:8000/api/employees/1/delete/ \
  -H "Authorization: Bearer <your_access_token>"
```

---

## Summary

### CRUD Operations Overview

✅ **Create:** `POST /api/employees/create/` → Add new employees with validation  
✅ **Read:** `GET /api/employees/` → List all employees with pagination and filtering  
✅ **Retrieve:** `GET /api/employees/{id}/` → Fetch individual employee records  
✅ **Update:** `PUT /api/employees/{id}/update/` → Modify employee details  
✅ **Delete:** `DELETE /api/employees/{id}/delete/` → Remove employees from the database  

### RESTful Best Practices

This API adheres to RESTful conventions:
- **HTTP Methods:** Correct use of POST (create), GET (read), PUT (update), DELETE (remove)
- **Status Codes:** Appropriate responses (200 OK, 201 Created, 204 No Content, 400 Bad Request, 404 Not Found)
- **Error Handling:** Clear, informative error messages for validation failures and not-found scenarios
- **Stateless Design:** Each request contains all necessary information; no server-side session dependencies

### Error Handling

The API provides meaningful error responses:
- **400 Bad Request:** Validation errors (e.g., duplicate email)
- **404 Not Found:** Resource doesn't exist
- **401 Unauthorized:** Missing or invalid token
- **500 Internal Server Error:** Unexpected server issues

### Postman for Easy Testing

Postman simplifies API testing:
1. Create a collection for the Employee API endpoints
2. Set up environment variables for `base_url` and `access_token`
3. Use pre-request scripts to automatically include the Bearer token
4. Save request examples for team collaboration
5. Run tests sequentially to verify the full CRUD workflow

---


