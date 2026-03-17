from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Student, Company, Placement

class PlacementAnalyticsE2ETest(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(username='testadmin', password='testpassword')
        self.client = Client()
        self.client.login(username='testadmin', password='testpassword')

    def test_end_to_end_journey(self):
        # 1. Access Dashboard
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')

        # 2. Add a Student
        student_data = {
            'name': 'Test Student',
            'email': 'teststudent@example.com',
            'branch': 'CSE',
            'passing_year': 2024,
            'cgpa': 8.5,
            'skills': 'Python, Django'
        }
        response = self.client.post(reverse('add_student'), data=student_data)
        if response.status_code != 302:
            print("Student form errors:", response.context.get('form').errors if response.context and 'form' in response.context else "Unknown error")
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.first().name, 'Test Student')

        # 3. Add a Company
        company_data = {
            'company_name': 'Test Company',
            'location': 'Bangalore',
            'website': 'https://testcompany.com',
            'role': 'SDE',
            'ctc': 12.0,
            'offer_type': 'Full-Time'
        }
        response = self.client.post(reverse('add_company'), data=company_data)
        if response.status_code != 302:
            print("Company form errors:", response.context.get('form').errors if response.context and 'form' in response.context else "Unknown error")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.first().company_name, 'Test Company')

        # 4. Add a Placement linking Student and Company
        student = Student.objects.first()
        company = Company.objects.first()
        placement_data = {
            'student': student.pk,
            'company': company.pk,
            'status': 'Placed',
            'package': 12.0,
            'placement_date': '2024-05-10'
        }
        response = self.client.post(reverse('add_placement'), data=placement_data)
        if response.status_code != 302:
            print("Placement form errors:", response.context.get('form').errors if response.context and 'form' in response.context else "Unknown error")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Placement.objects.count(), 1)
        self.assertEqual(Placement.objects.first().status, 'Placed')

        # 5. Access Analytics and ensure it doesn't crash with the new data
        response = self.client.get(reverse('analytics'))
        self.assertEqual(response.status_code, 200)
        
        # 6. Access lists to ensure data appears
        response_students = self.client.get(reverse('student_list'))
        self.assertContains(response_students, 'Test Student')

        response_companies = self.client.get(reverse('company_list'))
        self.assertContains(response_companies, 'Test Company')

        response_placements = self.client.get(reverse('placement_list'))
        self.assertContains(response_placements, 'Test Student')
        self.assertContains(response_placements, 'Test Company')

        print("All End-to-End tests executed successfully: Data flows correctly from inputs to lists and dashboard analytics!")

    def test_csv_upload(self):
        # Create a simple CSV file in memory
        from django.core.files.uploadedfile import SimpleUploadedFile
        csv_content = b"name,branch,cgpa,passing_year,skills,email,phone,internship_done\nAlice,CSE,9.0,2025,Python,alice@test.com,1234567890,Yes\nBob,IT,8.5,2025,Java,bob@test.com,0987654321,No"
        dataset = SimpleUploadedFile("students.csv", csv_content, content_type="text/csv")

        # Upload students dataset
        upload_url = reverse('upload_dataset')
        response = self.client.post(upload_url, {
            'dataset_type': 'student',
            'file': dataset
        })
        
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertEqual(Student.objects.filter(name__in=['Alice', 'Bob']).count(), 2)
        print("Dataset upload test executed successfully!")
