from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from .models import Student, Company, Placement
from .forms import StudentForm, CompanyForm, PlacementForm, DatasetUploadForm
from .utils import (
    process_student_csv,
    process_company_csv,
    process_placement_csv,
    get_dashboard_stats,
)
import json


# ─── Authentication ──────────────────────────────────────────────────────────

def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ─── Dashboard ───────────────────────────────────────────────────────────────

@login_required
def dashboard_view(request):
    """Main dashboard with KPI cards and summary stats."""
    # Cache dashboard stats for 5 minutes to avoid heavy DB queries on every load
    stats = cache.get('dashboard_stats')
    if stats is None:
        stats = get_dashboard_stats()
        cache.set('dashboard_stats', stats, 300)  # 300 seconds = 5 minutes

    # Prepare chart data as JSON for Chart.js
    branch_labels = json.dumps([b['branch'] for b in stats['branch_stats']])
    branch_placed = json.dumps([b['placed'] for b in stats['branch_stats']])
    branch_total = json.dumps([b['total'] for b in stats['branch_stats']])
    branch_rates = json.dumps([b['rate'] for b in stats['branch_stats']])

    company_names = json.dumps([c.company_name for c in stats['company_hiring']])
    company_hires = json.dumps([c.hire_count for c in stats['company_hiring']])

    offer_data = json.dumps([
        stats['fulltime_count'],
        stats['internship_count'],
        stats['both_count'],
    ])

    context = {
        **stats,
        'branch_labels': branch_labels,
        'branch_placed': branch_placed,
        'branch_total': branch_total,
        'branch_rates': branch_rates,
        'company_names': company_names,
        'company_hires': company_hires,
        'offer_data': offer_data,
        'recent_placements': Placement.objects.select_related('student', 'company')[:5],
    }
    return render(request, 'dashboard.html', context)


# ─── Students CRUD ───────────────────────────────────────────────────────────

@login_required
def student_list(request):
    """List students with search and pagination."""
    query = request.GET.get('q', '')
    students_qs = Student.objects.all()
    if query:
        students_qs = students_qs.filter(
            Q(name__icontains=query) |
            Q(branch__icontains=query) |
            Q(skills__icontains=query)
        )
    paginator = Paginator(students_qs, 25)  # 25 students per page
    page_number = request.GET.get('page', 1)
    try:
        students = paginator.page(page_number)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    return render(request, 'students/student_list.html', {
        'students': students,
        'query': query,
    })


@login_required
def add_student(request):
    """Add a new student."""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            cache.delete_many(['dashboard_stats', 'analytics_stats'])
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/add_student.html', {'form': form})


@login_required
def edit_student(request, pk):
    """Edit an existing student."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            cache.delete_many(['dashboard_stats', 'analytics_stats'])
            messages.success(request, 'Student updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/edit_student.html', {'form': form, 'student': student})


@login_required
def delete_student(request, pk):
    """Delete a student."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        cache.delete_many(['dashboard_stats', 'analytics_stats'])
        messages.success(request, 'Student deleted successfully!')
    return redirect('student_list')


# ─── Companies CRUD ──────────────────────────────────────────────────────────

@login_required
def company_list(request):
    """List companies with search and pagination."""
    query = request.GET.get('q', '')
    companies_qs = Company.objects.all()
    if query:
        companies_qs = companies_qs.filter(
            Q(company_name__icontains=query) |
            Q(role__icontains=query) |
            Q(location__icontains=query)
        )
    paginator = Paginator(companies_qs, 25)  # 25 companies per page
    page_number = request.GET.get('page', 1)
    try:
        companies = paginator.page(page_number)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)

    return render(request, 'companies/company_list.html', {
        'companies': companies,
        'query': query,
    })


@login_required
def add_company(request):
    """Add a new company."""
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            cache.delete_many(['dashboard_stats', 'analytics_stats'])
            messages.success(request, 'Company added successfully!')
            return redirect('company_list')
    else:
        form = CompanyForm()
    return render(request, 'companies/add_company.html', {'form': form})


@login_required
def edit_company(request, pk):
    """Edit an existing company."""
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            cache.delete_many(['dashboard_stats', 'analytics_stats'])
            messages.success(request, 'Company updated successfully!')
            return redirect('company_list')
    else:
        form = CompanyForm(instance=company)
    return render(request, 'companies/edit_company.html', {'form': form, 'company': company})


@login_required
def delete_company(request, pk):
    """Delete a company."""
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        company.delete()
        cache.delete_many(['dashboard_stats', 'analytics_stats'])
        messages.success(request, 'Company deleted successfully!')
    return redirect('company_list')


# ─── Placements CRUD ─────────────────────────────────────────────────────────

@login_required
def placement_list(request):
    """List placements with search and pagination."""
    query = request.GET.get('q', '')
    placements_qs = Placement.objects.select_related('student', 'company').all()
    if query:
        placements_qs = placements_qs.filter(
            Q(student__name__icontains=query) |
            Q(company__company_name__icontains=query) |
            Q(status__icontains=query)
        )
    paginator = Paginator(placements_qs, 25)  # 25 placements per page
    page_number = request.GET.get('page', 1)
    try:
        placements = paginator.page(page_number)
    except PageNotAnInteger:
        placements = paginator.page(1)
    except EmptyPage:
        placements = paginator.page(paginator.num_pages)

    return render(request, 'placements/placement_list.html', {
        'placements': placements,
        'query': query,
    })


@login_required
def add_placement(request):
    """Add a new placement."""
    if request.method == 'POST':
        form = PlacementForm(request.POST)
        if form.is_valid():
            form.save()
            cache.delete_many(['dashboard_stats', 'analytics_stats'])
            messages.success(request, 'Placement record added successfully!')
            return redirect('placement_list')
    else:
        form = PlacementForm()
    return render(request, 'placements/add_placement.html', {'form': form})


@login_required
def edit_placement(request, pk):
    """Edit an existing placement."""
    placement = get_object_or_404(Placement, pk=pk)
    if request.method == 'POST':
        form = PlacementForm(request.POST, instance=placement)
        if form.is_valid():
            form.save()
            cache.delete_many(['dashboard_stats', 'analytics_stats'])
            messages.success(request, 'Placement record updated successfully!')
            return redirect('placement_list')
    else:
        form = PlacementForm(instance=placement)
    return render(request, 'placements/edit_placement.html', {'form': form, 'placement': placement})


@login_required
def delete_placement(request, pk):
    """Delete a placement."""
    placement = get_object_or_404(Placement, pk=pk)
    if request.method == 'POST':
        placement.delete()
        cache.delete_many(['dashboard_stats', 'analytics_stats'])
        messages.success(request, 'Placement record deleted successfully!')
    return redirect('placement_list')


# ─── Dataset Upload ──────────────────────────────────────────────────────────

@login_required
def upload_dataset(request):
    """Handle bulk CSV dataset upload."""
    if request.method == 'POST':
        form = DatasetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            dataset_type = form.cleaned_data['dataset_type']
            file = request.FILES['file']

            processors = {
                'student': process_student_csv,
                'company': process_company_csv,
                'placement': process_placement_csv,
            }

            processor = processors.get(dataset_type)
            if processor:
                count, errors = processor(file)
                if count > 0:
                    cache.delete_many(['dashboard_stats', 'analytics_stats'])
                    messages.success(request, f'Successfully imported {count} {dataset_type} records.')
                if errors:
                    for error in errors[:10]:
                        messages.warning(request, error)
                    if len(errors) > 10:
                        messages.warning(request, f'... and {len(errors) - 10} more errors.')
            else:
                messages.error(request, 'Invalid dataset type.')

            return redirect('upload_dataset')
    else:
        form = DatasetUploadForm()

    return render(request, 'upload_dataset.html', {'form': form})


# ─── Analytics ───────────────────────────────────────────────────────────────

@login_required
def analytics_view(request):
    """Analytics page with chart data."""
    # Cache analytics stats for 5 minutes
    stats = cache.get('analytics_stats')
    if stats is None:
        stats = get_dashboard_stats()
        cache.set('analytics_stats', stats, 300)

    branch_labels = json.dumps([b['branch'] for b in stats['branch_stats']])
    branch_placed = json.dumps([b['placed'] for b in stats['branch_stats']])
    branch_total = json.dumps([b['total'] for b in stats['branch_stats']])
    branch_rates = json.dumps([b['rate'] for b in stats['branch_stats']])

    company_names = json.dumps([c.company_name for c in stats['company_hiring']])
    company_hires = json.dumps([c.hire_count for c in stats['company_hiring']])

    offer_data = json.dumps([
        stats['fulltime_count'],
        stats['internship_count'],
        stats['both_count'],
    ])

    # ✅ Salary distribution in a single conditional-count query
    salary_aggs = Placement.objects.filter(status='Placed').aggregate(
        r0_5=Count('placement_id', filter=Q(package__lt=5)),
        r5_10=Count('placement_id', filter=Q(package__gte=5, package__lt=10)),
        r10_15=Count('placement_id', filter=Q(package__gte=10, package__lt=15)),
        r15_20=Count('placement_id', filter=Q(package__gte=15, package__lt=20)),
        r20p=Count('placement_id', filter=Q(package__gte=20)),
    )
    salary_ranges = {
        '0-5 LPA':   salary_aggs['r0_5'],
        '5-10 LPA':  salary_aggs['r5_10'],
        '10-15 LPA': salary_aggs['r10_15'],
        '15-20 LPA': salary_aggs['r15_20'],
        '20+ LPA':   salary_aggs['r20p'],
    }

    context = {
        **stats,
        'branch_labels': branch_labels,
        'branch_placed': branch_placed,
        'branch_total': branch_total,
        'branch_rates': branch_rates,
        'company_names': company_names,
        'company_hires': company_hires,
        'offer_data': offer_data,
        'salary_range_labels': json.dumps(list(salary_ranges.keys())),
        'salary_range_data': json.dumps(list(salary_ranges.values())),
    }
    return render(request, 'analytics.html', context)
