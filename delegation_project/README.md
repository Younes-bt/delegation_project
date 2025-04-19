# Delegation Project

A comprehensive Django-based Learning Management System (LMS) for managing educational institutions, training centers, and their associated resources.

## Features

### 1. User Management
- Multi-role user system (Superuser, Center Manager, Teacher, Student, Center Staff)
- JWT-based authentication
- Profile management for all users
- Role-based permissions and access control
- Admin-only user creation

### 2. Training Management
- Course and training program management
- Training group organization
- Student enrollment tracking
- Material and resource management

### 3. Class Timetable
- Schedule management for classes
- Teacher availability tracking
- Room allocation
- Recurring class scheduling
- Holiday and exception handling

### 4. Attendance System
- Real-time attendance tracking
- Multiple attendance statuses (Present, Absent, Late, Excused)
- Attendance reports and analytics
- Historical attendance data

### 5. Reporting System
- Comprehensive attendance reporting
- Multiple report types:
  - Student Reports
  - Teacher Reports
  - Group Reports
  - Center Reports
- Statistical analysis and trends
- Customizable date ranges
- Export capabilities

## Technical Stack

- **Backend**: Django 5.2
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **CORS**: django-cors-headers
- **Filtering**: django-filter

## Project Structure

```
delegation_project/
├── accounts/                 # User management app
├── training/                 # Training and course management
├── class_timetable/         # Schedule management
├── attendance_reports/       # Attendance tracking
├── reports/                 # Analytics and reporting
└── delegation_project/      # Main project settings
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd delegation_project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with:
```
DJANGO_SECRET_KEY=your_secret_key
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## API Documentation

### Authentication

All endpoints except for login require JWT authentication.

#### Obtain Token
```
POST /accounts/token/
{
    "email": "user@example.com",
    "password": "password"
}
```

#### Refresh Token
```
POST /accounts/token/refresh/
{
    "refresh": "refresh_token"
}
```

### User Management

#### Create User (Admin Only)
```
POST /accounts/admin/users/create/
{
    "email": "user@example.com",
    "password": "password",
    "role": "STUDENT"
}
```
Note: This endpoint is restricted to admin users only.

#### User Profile
```
GET /accounts/users/{id}/
```

### Training Management

#### Training Programs
```
GET /training/programs/
POST /training/programs/
GET /training/programs/{id}/
PUT /training/programs/{id}/
DELETE /training/programs/{id}/
```

### Class Timetable

#### Schedule Entries
```
GET /api/timetable/schedules/
POST /api/timetable/schedules/
GET /api/timetable/schedules/{id}/
PUT /api/timetable/schedules/{id}/
DELETE /api/timetable/schedules/{id}/
```

### Attendance System

#### Record Attendance
```
POST /api/attendance/record/
{
    "student": 1,
    "schedule": 1,
    "status": "PRESENT",
    "date": "2024-04-14"
}
```

### Reporting System

#### Generate Reports
```
POST /api/reports/reports/
{
    "report_type": "STUDENT",
    "period": "MONTHLY",
    "start_date": "2024-04-01",
    "end_date": "2024-04-30",
    "student_id": 1
}
```

#### Quick Statistics
```
GET /api/reports/reports/quick_stats/
```

#### My Reports
```
GET /api/reports/reports/my_reports/
```

## Permissions

### Role-Based Access

1. **Superuser**
   - Full access to all features
   - Can manage all users and centers
   - Can create new users

2. **Center Manager**
   - Manage center staff and teachers
   - View and generate center reports
   - Manage center resources

3. **Teacher**
   - Record attendance
   - View student reports
   - Manage class schedules
   - Generate reports for their classes

4. **Student**
   - View their attendance
   - Access their reports
   - View their schedule

5. **Center Staff**
   - Manage resources
   - View center reports
   - Basic administrative tasks

## Data Models

### User Models
- CustomUser
- UserProfile
- Center
- Association
- Training
- TrainingGroup

### Schedule Models
- ScheduleEntry
- TeacherAvailability
- Holiday

### Attendance Models
- Attendance
- AttendanceReport

### Report Models
```python
class AttendanceReport:
    - report_type (STUDENT/TEACHER/GROUP/CENTER)
    - period (DAILY/WEEKLY/MONTHLY/CUSTOM)
    - start_date, end_date
    - targets (student/teacher/group/center)
    - statistics (attendance rates, sessions, etc.)
    - detailed data (JSON)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 