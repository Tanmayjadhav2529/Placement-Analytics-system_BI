from django import forms
from .models import Student, Company, Placement


class StudentForm(forms.ModelForm):
    """Form for adding/editing student records."""

    class Meta:
        model = Student
        fields = ['name', 'branch', 'cgpa', 'passing_year', 'skills', 'internship_done', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter student name',
            }),
            'branch': forms.Select(attrs={
                'class': 'form-select',
            }),
            'cgpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 8.50',
                'step': '0.01',
                'min': '0',
                'max': '10',
            }),
            'passing_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 2025',
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Python, Java, Machine Learning',
                'rows': 3,
            }),
            'internship_done': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'student@example.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 9876543210',
            }),
        }


class CompanyForm(forms.ModelForm):
    """Form for adding/editing company records."""

    class Meta:
        model = Company
        fields = ['company_name', 'role', 'ctc', 'location', 'offer_type', 'website']
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name',
            }),
            'role': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Software Engineer',
            }),
            'ctc': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 12.00',
                'step': '0.01',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Bangalore',
            }),
            'offer_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://company.com',
            }),
        }


class PlacementForm(forms.ModelForm):
    """Form for adding/editing placement records."""

    class Meta:
        model = Placement
        fields = ['student', 'company', 'package', 'status', 'placement_date']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-select',
            }),
            'company': forms.Select(attrs={
                'class': 'form-select',
            }),
            'package': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 10.00',
                'step': '0.01',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'placement_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }


class DatasetUploadForm(forms.Form):
    """Form for uploading CSV/Excel datasets."""

    DATASET_TYPE_CHOICES = [
        ('student', 'Student Dataset'),
        ('company', 'Company Dataset'),
        ('placement', 'Placement Dataset'),
    ]

    dataset_type = forms.ChoiceField(
        choices=DATASET_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv,.xlsx,.xls',
        }),
        help_text='Upload a CSV or Excel file.',
    )
