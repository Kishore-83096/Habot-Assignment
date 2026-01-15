# HABOT Employee Management System

A full-stack web application for managing employee data with a modern React frontend and a robust Django REST API backend.

## 🚀 Features

- **Employee CRUD Operations**: Create, read, update, and delete employee records
- **JWT Authentication**: Secure token-based authentication system
- **Responsive UI**: Modern React interface with intuitive navigation
- **API Documentation**: Comprehensive API endpoints with examples
- **Filtering & Pagination**: Advanced employee listing with department and role filters
- **Data Validation**: Server-side validation with meaningful error messages

## 🛠 Tech Stack

### Backend
- **Django 6.0.1** - Web framework
- **Django REST Framework 3.16.1** - API framework
- **JWT Authentication** - Secure token-based auth
- **SQLite** - Database (development)
- **Gunicorn** - WSGI server

### Frontend
- **React 19.2.0** - UI library
- **Vite 7.2.4** - Build tool and dev server
- **React Router 7.12.0** - Client-side routing
- **ESLint** - Code linting

## 📁 Project Structure

```
HABOT PROJECT/
├── backend/                 # Django REST API
│   ├── config/             # Main Django app
│   │   └── api/           # API views and URLs
│   ├── api_endpoints.md    # API documentation
│   ├── requirements.txt    # Python dependencies
│   └── venv/              # Virtual environment
└── frontend/               # React application
    ├── src/
    │   ├── api/           # API client and endpoints
    │   ├── components/    # Reusable components
    │   ├── pages/         # Page components
    │   └── routes/        # Routing configuration
    ├── package.json       # Node dependencies
    └── vite.config.js     # Vite configuration
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd HABOT PROJECT/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd HABOT FRONTEND/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173/`

## 📚 API Documentation

Detailed API documentation is available in [`backend/api_endpoints.md`](backend/api_endpoints.md), including:

- Authentication endpoints (token obtain/refresh)
- Employee CRUD operations
- Filtering and pagination
- Error handling examples
- cURL examples for testing

### Quick API Overview

#### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh access token

#### Employee Operations
- `GET /api/employees/` - List employees (with filtering)
- `POST /api/employees/create/` - Create new employee
- `GET /api/employees/{id}/` - Get employee details
- `PUT /api/employees/{id}/update/` - Update employee
- `DELETE /api/employees/{id}/delete/` - Delete employee

## 🎯 Usage

1. **Start both backend and frontend servers** as described above
2. **Access the frontend** at `http://localhost:5173/`
3. **Login** using credentials created during backend setup
4. **Manage employees** through the intuitive web interface:
   - View employee list with pagination
   - Filter by department or role
   - Create new employees
   - Update existing employee details
   - Delete employees

## 🔒 Authentication

The application uses JWT (JSON Web Tokens) for authentication:
- Obtain tokens via `/api/token/` endpoint
- Include `Authorization: Bearer <token>` header in API requests
- Tokens expire and need refreshing via `/api/token/refresh/`

## 🧪 Testing

### Backend Tests
```bash
cd HABOT PROJECT/backend
python manage.py test
```

### Frontend Linting
```bash
cd HABOT FRONTEND/frontend
npm run lint
```

## 🚀 Deployment

### Backend Deployment
1. Set `DEBUG=False` in Django settings
2. Configure production database (PostgreSQL recommended)
3. Use Gunicorn for production serving
4. Set up environment variables for secrets

### Frontend Deployment
1. Build the production bundle:
   ```bash
   npm run build
   ```
2. Deploy the `dist/` folder to your hosting service
3. Configure API base URL for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or issues, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ using Django, React, and modern web technologies.**
