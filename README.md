<<<<<<< HEAD
# Placement-Analytics-system_BI
Placement &amp; Internship Analytics System is a web application built using Django, SQL, and Power BI to manage and analyze college placement data. It allows administrators to store student, company, and placement records, upload datasets in bulk, and generate interactive analytics dashboards to visualize hiring trends and placement insights.
=======
# Placement & Internship Analytics System

A comprehensive Django-based application designed to manage and analyze student placements and internships. The system allows institutions to maintain records of students, recruiting companies, and placement offers, as well as visualize hiring trends and salary distributions.

## Features

### 1. Robust Database Architecture
- **Student Management:** Tracks student details such as ID, name, branch (CSE, IT, ECE, EEE, ME, CE), CGPA, passing year, skills, internship status, and contact information.
- **Company Tracking:** Stores recruiting company information including company name, role offered, package/CTC in LPA, location, and the type of offer (Full-Time, Internship, or Both).
- **Placement Records:** Links students to companies to maintain real-time placement status (Placed, Not Placed, In Progress), package details, and placement dates.

### 2. User Authentication & Security
- Secure login and logout flows to ensure only authorized personnel can access and manage the placement data.

### 3. Comprehensive CRUD Capabilities
Complete management interface with Create, Read, Update, and Delete options:
- **Students:** Add, edit, remove, and search students by name, branch, or skills.
- **Companies:** Manage participating companies and search by company name, role, or location.
- **Placements:** Centralized view for establishing connections between a student and a company, with search fields for quick lookup.

### 4. Bulk Data Upload functionality
- An integrated CSV Import System to bulk-insert student, company, or placement records.
- Built-in validation and error handling providing immediate feedback on invalid dataset rows.

### 5. Interactive Dashboard & Analytics
- Meaningful Key Performance Indicators (KPIs) available at a glance.
- Integration with **Chart.js** to provide dynamic visual insights:
    - **Branch-wise Statistics:** Placement rates and total students placed per branch.
    - **Top Hiring Companies:** Visualizes which companies are actively hiring.
    - **Offer Types Breakdown:** Analyzes the distribution of full-time vs. internship offers.
    - **Salary Distribution:** A histogram-like breakdown of salary buckets (e.g., 0-5 LPA, 5-10 LPA, 10-15 LPA, etc.).

### 6. Modern Frontend Interface
- Implemented using a scalable layout structure with intuitive styling and responsive design. Dedicated pages for dashboard, individual CRUD actions, data upload, and detailed analytics.

## Getting Started

### Prerequisites

- Python 3.8+
- Django 4.x or above
- SQLite (Uses default Django configuration)

### Installation

1. Clone this repository
2. Navigate to the project directory:
   ```bash
   cd placement_analytics_system
   ```
3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Mac/Linux
   source venv/bin/activate
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Create an admin superuser to manage the initial state:
   ```bash
   python manage.py createsuperuser
   ```
7. Start the development server:
   ```bash
   python manage.py runserver
   ```
8. Access the system via `http://localhost:8000/`. You can log in with the superuser credentials.

## Directory Structure

- `placement_app/`: Holds the core Django application code (Models, Views, Forms, URLs).
- `placement_app/templates/`: Stores the HTML templates organizing layouts, analytics dashboards, and management screens.
- `datasets/`: Includes sample CSV datasets for testing bulk uploads.
- `docs/`: Includes documentation (if any) or related product requirements documents.
- `placement_analytics_system/`: The root Django configuration (Settings, WSGI, URL routing).

---
*Built to streamline the placement cell's workflow from data entry to data analysis.*
>>>>>>> 75b75f0 (First time add)
