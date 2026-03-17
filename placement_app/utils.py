"""Utility functions for data processing and CSV/Excel imports."""
import csv
import io
from decimal import Decimal, InvalidOperation
from .models import Student, Company, Placement


def process_student_csv(file):
    """Process uploaded CSV file and import student records."""
    decoded_file = file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded_file))
    count = 0
    errors = []

    for i, row in enumerate(reader, start=2):
        try:
            Student.objects.create(
                name=row.get('name', '').strip(),
                branch=row.get('branch', 'CSE').strip(),
                cgpa=Decimal(row.get('cgpa', '0').strip()),
                passing_year=int(row.get('passing_year', '2025').strip()),
                skills=row.get('skills', '').strip(),
                internship_done=row.get('internship_done', 'False').strip().lower() in ('true', '1', 'yes'),
                email=row.get('email', '').strip() or None,
                phone=row.get('phone', '').strip() or None,
            )
            count += 1
        except (ValueError, InvalidOperation) as e:
            errors.append(f"Row {i}: {str(e)}")

    return count, errors


def process_company_csv(file):
    """Process uploaded CSV file and import company records."""
    decoded_file = file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded_file))
    count = 0
    errors = []

    for i, row in enumerate(reader, start=2):
        try:
            Company.objects.create(
                company_name=row.get('company_name', '').strip(),
                role=row.get('role', '').strip(),
                ctc=Decimal(row.get('ctc', '0').strip()),
                location=row.get('location', '').strip(),
                offer_type=row.get('offer_type', 'Full-Time').strip(),
                website=row.get('website', '').strip() or None,
            )
            count += 1
        except (ValueError, InvalidOperation) as e:
            errors.append(f"Row {i}: {str(e)}")

    return count, errors


def process_placement_csv(file):
    """Process uploaded CSV file and import placement records."""
    decoded_file = file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded_file))
    count = 0
    errors = []

    # Pre-load all students and companies into dicts to avoid N+1 per-row queries
    student_map = {s.student_id: s for s in Student.objects.all()}
    company_map = {c.company_id: c for c in Company.objects.all()}

    placements_to_create = []
    for i, row in enumerate(reader, start=2):
        try:
            student_id = int(row.get('student_id', '0').strip())
            company_id = int(row.get('company_id', '0').strip())
            student = student_map.get(student_id)
            company = company_map.get(company_id)
            if not student:
                errors.append(f"Row {i}: Student with id {student_id} not found.")
                continue
            if not company:
                errors.append(f"Row {i}: Company with id {company_id} not found.")
                continue
            placements_to_create.append(Placement(
                student=student,
                company=company,
                package=Decimal(row.get('package', '0').strip()),
                status=row.get('status', 'In Progress').strip(),
                placement_date=row.get('placement_date', None) or None,
            ))
            count += 1
        except (ValueError, InvalidOperation) as e:
            errors.append(f"Row {i}: {str(e)}")

    if placements_to_create:
        Placement.objects.bulk_create(placements_to_create)

    return count, errors


def get_dashboard_stats():
    """Calculate dashboard statistics with optimized queries."""
    from django.db.models import Avg, Max, Min, Count, Q

    total_students = Student.objects.count()
    total_companies = Company.objects.count()
    total_placements = Placement.objects.filter(status='Placed').count()

    # ✅ Combine three separate aggregations into a single DB query
    salary_aggs = Placement.objects.filter(status='Placed').aggregate(
        avg=Avg('package'),
        max=Max('package'),
        min=Min('package'),
    )
    avg_salary = salary_aggs['avg'] or 0
    max_salary = salary_aggs['max'] or 0
    min_salary = salary_aggs['min'] or 0

    placement_rate = round((total_placements / total_students * 100), 1) if total_students > 0 else 0

    # ✅ Fix N+1: Replace the for-loop with a single annotated query
    branch_qs = Student.objects.values('branch').annotate(
        total=Count('student_id'),
        placed=Count(
            'placements',
            filter=Q(placements__status='Placed')
        )
    ).order_by('branch')

    branch_stats = []
    for b in branch_qs:
        branch_total = b['total']
        branch_placed = b['placed']
        branch_rate = round((branch_placed / branch_total * 100), 1) if branch_total > 0 else 0
        branch_stats.append({
            'branch': b['branch'],
            'total': branch_total,
            'placed': branch_placed,
            'rate': branch_rate,
        })

    # Company-wise hiring count — already an efficient single annotated query
    company_hiring = Company.objects.annotate(
        hire_count=Count('placements', filter=Q(placements__status='Placed'))
    ).filter(hire_count__gt=0).order_by('-hire_count')[:10]

    # ✅ Combine three offer-type counts into a single query via conditional Count
    offer_aggs = Placement.objects.filter(status='Placed').aggregate(
        fulltime=Count('placement_id', filter=Q(company__offer_type='Full-Time')),
        internship=Count('placement_id', filter=Q(company__offer_type='Internship')),
        both=Count('placement_id', filter=Q(company__offer_type='Both')),
    )

    return {
        'total_students': total_students,
        'total_companies': total_companies,
        'total_placements': total_placements,
        'avg_salary': round(float(avg_salary), 2),
        'max_salary': round(float(max_salary), 2),
        'min_salary': round(float(min_salary), 2),
        'placement_rate': placement_rate,
        'branch_stats': branch_stats,
        'company_hiring': company_hiring,
        'fulltime_count': offer_aggs['fulltime'],
        'internship_count': offer_aggs['internship'],
        'both_count': offer_aggs['both'],
    }
