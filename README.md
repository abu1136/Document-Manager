# Document Management System

A web-based Document Management System designed to generate and manage official company documents using standardized letterhead templates.

## Features

- **User Authentication**: Secure login with JWT tokens
- **Role-Based Access**: Admin and user roles with different permissions
- **Document Generation**: Create PDF and DOCX documents with custom content
- **Letterhead Management**: Upload and manage company letterhead templates
- **Document Tracking**: Track who created each document with automatic numbering
- **Document History**: View and filter document history
- **User Management**: Admin can create users and reset passwords

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MySQL 8 with SQLAlchemy ORM
- **Authentication**: JWT with bcrypt password hashing
- **Document Generation**: 
  - PDF: ReportLab + PyMuPDF
  - DOCX: python-docx

### Frontend
- **HTML/CSS/JavaScript** (Vanilla)
- **No framework dependencies**

## Setup and Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd Document-Manager
```

2. Start the application:
```bash
docker-compose up -d
```

3. **IMPORTANT - Database Migration (if upgrading from older version):**
   
   If you're upgrading from an older version and getting errors when creating users, you need to run the database migration:
   
   ```bash
   # Option 1: Run migration inside the container
   docker-compose exec backend python migrate_database.py
   
   # Option 2: Recreate the database (will lose all data)
   docker-compose down -v
   docker-compose up -d
   ```

4. Access the application:
- Navigate to `http://localhost:8000/ui/setup.html`
- Create the initial admin user
- Login at `http://localhost:8000/ui/login.html`

### Manual Installation

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set up MySQL database:
```bash
mysql -u root -p < ../sql/init.sql
```

3. Configure environment variables:
```bash
export DATABASE_URL="mysql+pymysql://docuser:docpass@localhost:3306/document_manager"
export JWT_SECRET="your-secret-key"
```

4. Run the application:
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Project Structure

```
Document-Manager/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── database.py          # Database configuration
│   │   ├── models/              # SQLAlchemy models
│   │   ├── routers/             # API endpoints
│   │   ├── services/            # Business logic (PDF/DOCX generation)
│   │   ├── utils/               # Utility functions
│   │   └── middleware/          # Authentication middleware
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile
├── frontend/
│   └── ui/                      # HTML templates and static files
│       ├── *.html               # Page templates
│       ├── js/                  # JavaScript files
│       └── css/                 # Stylesheets
├── sql/
│   └── init.sql                 # Database initialization script
└── docker-compose.yml           # Docker orchestration
```

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `GET /auth/setup/status` - Check if initial setup is required
- `POST /auth/setup` - Create initial admin user

### Documents
- `POST /documents/create` - Create a new document
- `GET /documents/history` - Get document history

### Admin
- `POST /admin/create-user` - Create a new user
- `GET /admin/users` - List all users
- `POST /admin/reset-password` - Reset user password
- `POST /admin/letterhead` - Upload letterhead template

### Profile
- `POST /profile/change-password` - Change current user's password

## Usage

### Initial Setup

1. Access the setup page to create the first admin user
2. Login with admin credentials
3. Upload a letterhead template (PDF format)
4. Create additional users as needed

### Creating Documents

1. Login as a user
2. Navigate to "Create Document"
3. Enter document title and content
4. Click "Generate Document"
5. Download PDF or DOCX versions

### Admin Tasks

- **User Management**: Create users, reset passwords
- **Letterhead Management**: Upload new letterhead templates
- **Document History**: View all documents created by all users

## Security Features

- JWT-based authentication
- Bcrypt password hashing
- Role-based access control
- Filename sanitization to prevent directory traversal
- SQL injection protection via SQLAlchemy ORM

## Database Schema

### Tables

- **users**: User accounts (id, username, password, role)
- **documents**: Document records (id, document_number, title, paths, created_by)
- **letterhead**: Letterhead templates (id, filename, filetype, uploaded_by, active)

## Troubleshooting

### Unable to Create Users

If you're getting errors when trying to create users after updating the code, this is likely due to a database schema mismatch. The column name was changed from `password_hash` to `password`.

**Solution 1: Run the migration script (recommended)**
```bash
# If using Docker
docker-compose exec backend python migrate_database.py

# If running manually
cd backend
python migrate_database.py
```

**Solution 2: Recreate the database (will lose all data)**
```bash
# If using Docker
docker-compose down -v
docker-compose up -d

# If running manually
mysql -u root -p -e "DROP DATABASE IF EXISTS document_manager;"
mysql -u root -p < sql/init.sql
```

### Other Common Issues

**Database Connection Errors:**
- Ensure MySQL is running
- Check the DATABASE_URL environment variable
- Verify MySQL credentials (docuser:docpass)

**Authentication Errors:**
- Clear browser localStorage and try logging in again
- Check that JWT_SECRET is set in environment variables

**File Upload Issues:**
- Ensure the `files/` directory exists and is writable
- Check that uploaded filenames don't contain special characters

## Recent Fixes

This repository has been audited and fixed for the following issues:

### Backend Fixes
- Fixed User model field naming consistency (password vs password_hash)
- Standardized authentication token handling
- Added missing setup endpoints
- Implemented proper Form data handling
- Added filename sanitization for security
- Standardized function parameter order

### Frontend Fixes
- Added missing JavaScript functions
- Created user_create.html for document creation
- Fixed API call formats and headers
- Ensured all navigation buttons work correctly

### Security Improvements
- Added filename sanitization
- Implemented directory traversal prevention
- CodeQL security scan passed with 0 alerts

## License

This project is licensed under the MIT License.

## Support

For issues or questions, please open an issue in the repository.
