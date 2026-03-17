import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_analytics_system.settings')
django.setup()

from placement_app.models import Student, Company, Placement

def clear_data():
    print("Deleting all mock data...")
    Placement.objects.all().delete()
    Student.objects.all().delete()
    Company.objects.all().delete()
    print("All mock data deleted!")

if __name__ == "__main__":
    clear_data()
