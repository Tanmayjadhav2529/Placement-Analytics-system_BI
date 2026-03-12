import os

base_dir = r"d:\placement\placement_analytics_system"

dirs = [
    "placement_analytics_system",
    "placement_app/migrations",
    "placement_app/templates/students",
    "placement_app/templates/companies",
    "placement_app/templates/placements",
    "placement_app/static/css",
    "placement_app/static/js",
    "placement_app/static/images",
    "datasets",
    "powerbi",
    "docs",
]

files = [
    "manage.py",
    "placement_analytics_system/__init__.py",
    "placement_analytics_system/settings.py",
    "placement_analytics_system/urls.py",
    "placement_analytics_system/asgi.py",
    "placement_analytics_system/wsgi.py",
    "placement_app/migrations/__init__.py",
    "placement_app/templates/base.html",
    "placement_app/templates/login.html",
    "placement_app/templates/dashboard.html",
    "placement_app/templates/students/student_list.html",
    "placement_app/templates/students/add_student.html",
    "placement_app/templates/students/edit_student.html",
    "placement_app/templates/companies/company_list.html",
    "placement_app/templates/companies/add_company.html",
    "placement_app/templates/companies/edit_company.html",
    "placement_app/templates/placements/placement_list.html",
    "placement_app/templates/placements/add_placement.html",
    "placement_app/templates/placements/edit_placement.html",
    "placement_app/templates/upload_dataset.html",
    "placement_app/static/css/styles.css",
    "placement_app/static/js/scripts.js",
    "placement_app/models.py",
    "placement_app/views.py",
    "placement_app/forms.py",
    "placement_app/urls.py",
    "placement_app/admin.py",
    "placement_app/utils.py",
    "datasets/student_dataset.csv",
    "datasets/company_dataset.csv",
    "datasets/placement_dataset.csv",
    "powerbi/placement_dashboard.pbix",
    "docs/PRD.docx",
    "docs/system_architecture.png",
    "docs/er_diagram.png",
    "requirements.txt",
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

for f in files:
    path = os.path.join(base_dir, f)
    with open(path, 'w') as file:
        pass

print("Done")
