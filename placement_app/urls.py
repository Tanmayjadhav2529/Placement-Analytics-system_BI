from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('students/<int:pk>/delete/', views.delete_student, name='delete_student'),

    # Companies
    path('companies/', views.company_list, name='company_list'),
    path('companies/add/', views.add_company, name='add_company'),
    path('companies/<int:pk>/edit/', views.edit_company, name='edit_company'),
    path('companies/<int:pk>/delete/', views.delete_company, name='delete_company'),

    # Placements
    path('placements/', views.placement_list, name='placement_list'),
    path('placements/add/', views.add_placement, name='add_placement'),
    path('placements/<int:pk>/edit/', views.edit_placement, name='edit_placement'),
    path('placements/<int:pk>/delete/', views.delete_placement, name='delete_placement'),

    # Upload
    path('upload/', views.upload_dataset, name='upload_dataset'),

    # Analytics
    path('analytics/', views.analytics_view, name='analytics'),
]
