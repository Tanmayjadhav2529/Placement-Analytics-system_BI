from django.contrib import admin
from .models import Student, Company, Placement


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'branch', 'cgpa', 'passing_year', 'internship_done')
    list_filter = ('branch', 'passing_year', 'internship_done')
    search_fields = ('name', 'skills', 'email')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'company_name', 'role', 'ctc', 'location', 'offer_type')
    list_filter = ('offer_type', 'location')
    search_fields = ('company_name', 'role')


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ('placement_id', 'student', 'company', 'package', 'status', 'placement_date')
    list_filter = ('status',)
    search_fields = ('student__name', 'company__company_name')
