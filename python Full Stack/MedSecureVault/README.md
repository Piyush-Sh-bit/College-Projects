# MedSecureVault: Technical Overview & Operational Guide

## 1. Introduction

MedSecureVault is a secure, role-based Django web application for managing medical documents and user accounts. It supports three user roles—Admin, Doctor, and Patient—each with tailored dashboards and permissions. The system is designed for production use with Neon Postgres, ensuring robust data security and scalability.

---

## Screenshots

Below are example screenshots of key features and dashboards. Save your screenshots in `staticfiles/admin/img/` and update the filenames as needed.

### Login Page
![Login Page](staticfiles/admin/img/login_screenshot.png)

### Admin Dashboard
![Admin Dashboard](staticfiles/admin/img/admin_dashboard_screenshot.png)

### Doctor Dashboard
![Doctor Dashboard](staticfiles/admin/img/doctor_dashboard_screenshot.png)

### Patient Dashboard
![Patient Dashboard](staticfiles/admin/img/patient_dashboard_screenshot.png)

### Document Upload
![Document Upload](staticfiles/admin/img/document_upload_screenshot.png)

---

## 2. Architecture & Project Structure

### 2.1. Core Components

- **Django Framework**: Provides the MVC structure, authentication, and ORM.
- **Neon Postgres**: Cloud-based PostgreSQL database for all persistent data.
- **Virtual Environment**: Isolates dependencies and secures confidential info via `.env`.

### 2.2. Directory Layout

- `manage.py`: Django’s CLI entry point for server, migrations, and management.
- `medsecurevault/`: Project settings, URLs, and WSGI entry.
- `accounts/`: User management app (models, views, forms, decorators, templates).
- `documents/`: Document management app (models, views, forms, templates).
- `templates/`: Shared HTML templates (base layout).
- `requirements.txt`: Python dependencies.
- `.env`: Confidential environment variables (never shared publicly).

---

## 3. User Roles & Workflows

### 3.1. Admin

- **Dashboard**: Approve/disapprove doctors, manage users and documents.
- **Login**: Via secret admin code (see `accounts/views.py`).
- **Actions**: Can view all users, approve doctors, and access all documents.

### 3.2. Doctor

- **Dashboard**: View assigned patients, recent documents, and messages.
- **Approval Workflow**: New doctors require admin approval before accessing dashboard.
- **Messaging**: Can reply to patient messages.

### 3.3. Patient

- **Dashboard**: View own documents, assigned doctor, and send messages.
- **Document Upload**: Securely upload medical files.
- **Messaging**: Communicate with assigned doctor.

---

## 4. Database & Security

### 4.1. Database Setup

- **Neon Postgres**: Connection managed via `DATABASE_URL` in `.env`.
- **No SQLite**: Project is production-ready; SQLite is not permitted.
- **Custom User Model**: `accounts/models.py` defines roles and approval status.

### 4.2. Confidential Info

- **.env File**: Stores secrets, database URL, and debug settings.
- **Virtual Environment**: All Python commands run inside `.venv` for security.

---

## 5. Application Logic

### 5.1. Authentication & Registration

- **CustomUser Model**: Extends Django’s user with roles and approval.
- **Registration**: Patients and doctors register; doctors await approval.
- **Login**: Standard login for all users; admin login via secret code.

### 5.2. Dashboards

- **Role-Based Routing**: After login, users are redirected to their dashboard based on role.
- **Templates**: Each dashboard uses Bootstrap for responsive design.

### 5.3. Document Management

- **Upload**: Patients upload documents via `documents/forms.py`.
- **View & Delete**: Documents are listed, detailed, and can be deleted by authorized users.

### 5.4. Messaging

- **Patient-to-Doctor**: Patients send messages to assigned doctor.
- **Doctor Replies**: Doctors reply via dashboard; unread messages are highlighted.

### 5.5. Admin Controls

- **User Management**: Approve/disapprove doctors, view all users.
- **Document Oversight**: Access all uploaded documents.

---

## 6. Running the Project

### 6.1. Setup

1. **Clone the Repository**:  
   `git clone <repo-url>`

2. **Create Virtual Environment**:  
   ```powershell
   python -m venv .venv
   . .venv/Scripts/Activate.ps1
   ```

3. **Install Dependencies**:  
   ```powershell
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

4. **Configure .env**:  
   Create `.env` in the root with:
   ```
   DATABASE_URL=postgresql://<your-neon-credentials>
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=*
   ```

5. **Apply Migrations**:  
   ```powershell
   .venv\Scripts\python.exe manage.py makemigrations
   .venv\Scripts\python.exe manage.py migrate
   ```

6. **Run the Server**:  
   ```powershell
   .venv\Scripts\python.exe manage.py runserver
   ```

### 6.2. Admin Access

- **Login Code**: Default is `'987654321@1'` (see `accounts/views.py`).
- **Change Code/Password**: Edit in `accounts/views.py` as needed.

---

## 7. File-by-File Explanation

### 7.1. `manage.py`
- Django’s CLI tool for running the server, migrations, and other commands.

### 7.2. `medsecurevault/settings.py`
- Configures database, static/media files, security, installed apps, and loads secrets from `.env`.

### 7.3. `medsecurevault/urls.py`
- Root URL configuration; routes users to dashboards based on role.

### 7.4. `accounts/models.py`
- Defines `CustomUser` with roles and approval logic.
- Defines `Message` for patient-doctor communication.

### 7.5. `accounts/views.py`
- Handles registration, login, dashboards, profile, and approval logic.
- Implements admin code login and smart redirects.

### 7.6. `accounts/forms.py`
- Forms for registration, login, messaging, and doctor replies.

### 7.7. `accounts/decorators.py`
- Role-based access control for views (doctor, patient, admin).

### 7.8. `accounts/admin.py`
- Admin interface for user management and doctor approval.

### 7.9. `accounts/templates/accounts/`
- HTML templates for login, dashboards, profile, registration, etc.

### 7.10. `documents/models.py`
- Defines `Document` model linked to users.

### 7.11. `documents/views.py`
- Handles document upload, listing, detail, and deletion.

### 7.12. `documents/forms.py`
- Form for document upload.

### 7.13. `documents/admin.py`
- Admin interface for document management.

### 7.14. `templates/base.html`
- Main layout for all pages.

### 7.15. `requirements.txt`
- Lists all Python dependencies.

### 7.16. `.env`
- Stores confidential info (never shared publicly).

---

## 8. Security & Best Practices

- **Never share `.env` or credentials.**
- **Always use the virtual environment for Python commands.**
- **Use Neon Postgres for all environments; SQLite is not allowed.**
- **Keep dependencies up to date in `requirements.txt`.**
- **Use role-based decorators to protect sensitive views.**

---

## 9. Troubleshooting

- **Database Issues**: Check `.env` and `settings.py` for correct `DATABASE_URL`.
- **Static Files**: Run `python manage.py collectstatic` if static files are missing.
- **Admin Login**: Ensure admin code and password are set correctly in `accounts/views.py`.
- **Template Errors**: Confirm custom template tags are registered and loaded.

---

## 10. Conclusion

MedSecureVault is a robust, secure, and scalable Django application for medical document management. Its modular structure, role-based access, and production-ready database setup make it suitable for real-world deployment. Follow the setup and operational steps above for a smooth experience.

---

If you need further details on any specific file or workflow, let me know!
## Database Setup
This project uses Neon Postgres for production. For local development, SQLite is the default. To use Neon Postgres:
1. Create a `.env` file in the project root with:
   ```env
   DATABASE_URL=postgresql://neondb_owner:npg_TdU3Rc6OiuFe@ep-hidden-wave-a8et5uus-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=*
   ```
2. The database connection is managed in `medsecurevault/settings.py` using `django-environ`.

## Virtual Environment
A Python virtual environment is set up at `.venv`. Use the following command to activate it:
```powershell
. .venv/Scripts/Activate.ps1
```
Install dependencies with:
```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Admin Code Location
- The admin interface for users: `accounts/admin.py`
- The admin interface for documents: `documents/admin.py`

## Main Logic Files
- User management: `accounts/views.py`, `accounts/models.py`
- Document management: `documents/views.py`, `documents/models.py`
- Project configuration: `medsecurevault/settings.py`

## Uploading Code
- Use the virtual environment for all Python commands.
- Ensure all dependencies are listed in `requirements.txt`.
- For database migrations, use:
  ```powershell
  .venv\Scripts\python.exe manage.py makemigrations
  .venv\Scripts\python.exe manage.py migrate
  ```
- For running the server:
  ```powershell
  .venv\Scripts\python.exe manage.py runserver
  ```

## Confidentiality
Details about sensitive data and credentials should be kept secure and not shared publicly.



---
For any issues, check the configuration in `medsecurevault/settings.py` and ensure your `.env` file is correctly set up.
