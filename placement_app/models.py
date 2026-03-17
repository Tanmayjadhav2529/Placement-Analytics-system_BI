from django.db import models


class Student(models.Model):
    """Model for storing student information."""

    BRANCH_CHOICES = [
        ('CSE', 'Computer Science'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics & Communication'),
        ('EEE', 'Electrical & Electronics'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('OTHER', 'Other'),
    ]

    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, db_index=True)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES, default='CSE', db_index=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    passing_year = models.IntegerField(db_index=True)
    skills = models.TextField(blank=True, null=True, help_text="Comma-separated skills")
    internship_done = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.branch} - {self.passing_year})"


class Company(models.Model):
    """Model for storing company information."""

    OFFER_TYPE_CHOICES = [
        ('Full-Time', 'Full-Time'),
        ('Internship', 'Internship'),
        ('Both', 'Both'),
    ]

    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=300, db_index=True)
    role = models.CharField(max_length=200, db_index=True)
    ctc = models.DecimalField(max_digits=10, decimal_places=2, help_text="CTC in LPA")
    location = models.CharField(max_length=200, db_index=True)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES, default='Full-Time', db_index=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Companies"

    def __str__(self):
        return f"{self.company_name} - {self.role}"


class Placement(models.Model):
    """Model for tracking student placements."""

    STATUS_CHOICES = [
        ('Placed', 'Placed'),
        ('Not Placed', 'Not Placed'),
        ('In Progress', 'In Progress'),
    ]

    placement_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='placements')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='placements')
    package = models.DecimalField(max_digits=10, decimal_places=2, help_text="Package in LPA")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress', db_index=True)
    placement_date = models.DateField(blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.name} → {self.company.company_name} ({self.status})"
