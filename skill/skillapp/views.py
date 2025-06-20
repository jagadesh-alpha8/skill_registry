from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from skillapp.models import CandidateProfile, Year, CollegeType, College, Department, Course, TrainingProvider
from django.http import HttpResponse
import openpyxl

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('my_home') 

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('rec')  
            else:
                messages.error(request, "Invalid password")
        except User.DoesNotExist:
            messages.error(request, "Email not registered")
        return render(request, 'login_page.html')
    return render(request, 'login_page.html')


def get_candidate_context(request):
    selected = {
        'year': '',
        'college_type': '',
        'department': '',
        'course': '',
        'tp': '',
    }

    show_results = False
    candidates = CandidateProfile.objects.none()
    eng = CandidateProfile.objects.filter(college_type__type_name="ENGINNERING").count()
    poly = CandidateProfile.objects.filter(college_type__type_name="POLYTECHNIC").count()
    arts = CandidateProfile.objects.filter(college_type__type_name="ARTS AND SCIENCE").count()
    iti = CandidateProfile.objects.filter(college_type__type_name="ITI").count()

    if request.method == 'POST':
        selected['year'] = request.POST.get('year', '')
        selected['college_type'] = request.POST.get('college_type', '')
        selected['department'] = request.POST.get('department', '')
        selected['course'] = request.POST.get('course', '')
        selected['tp'] = request.POST.get('tp', '')

        if 'search' in request.POST:
            if not all(selected.values()):
                messages.error(request, "Please select all fields before searching.")
            else:
                show_results = True

        filters = {}
        if selected['year']:
            filters['year__name'] = selected['year']
        if selected['college_type']:
            filters['college_type__type_name'] = selected['college_type']
        if selected['department']:
            filters['department__dept_name'] = selected['department']
        if selected['course']:
            filters['course__course_name'] = selected['course']
        if selected['tp']:
            filters['tp__tp_name'] = selected['tp']

        candidates = CandidateProfile.objects.filter(**filters)

        def get_filtered_options(exclude_field=None):
            temp_filters = {}
            if exclude_field != 'year' and selected['year']:
                temp_filters['year__name'] = selected['year']
            if exclude_field != 'college_type' and selected['college_type']:
                temp_filters['college_type__type_name'] = selected['college_type']
            if exclude_field != 'department' and selected['department']:
                temp_filters['department__dept_name'] = selected['department']
            if exclude_field != 'course' and selected['course']:
                temp_filters['course__course_name'] = selected['course']
            if exclude_field != 'tp' and selected['tp']:
                temp_filters['tp__tp_name'] = selected['tp']

            return CandidateProfile.objects.filter(**temp_filters) if temp_filters else CandidateProfile.objects.all()

        years = Year.objects.filter(candidateprofile__in=get_filtered_options('year')).distinct().order_by('name')
        college_types = CollegeType.objects.filter(candidateprofile__in=get_filtered_options('college_type')).distinct().order_by('type_name')
        departments = Department.objects.filter(candidateprofile__in=get_filtered_options('department')).distinct().order_by('dept_name')
        courses = Course.objects.filter(candidateprofile__in=get_filtered_options('course')).distinct().order_by('course_name')
        tps = TrainingProvider.objects.filter(candidateprofile__in=get_filtered_options('tp')).distinct().order_by('tp_name')

    else:
        years = Year.objects.all().distinct().order_by('name')
        college_types = CollegeType.objects.all().distinct().order_by('type_name')
        departments = Department.objects.all().distinct().order_by('dept_name')
        courses = Course.objects.all().distinct().order_by('course_name')
        tps = TrainingProvider.objects.all().distinct().order_by('tp_name')

    return {
        'years': years,
        'college_types': college_types,
        'departments': departments,
        'courses': courses,
        'tps': tps,
        'selected': selected,
        'candidate_count': candidates.count() if show_results else 0,
        'candidates': candidates if show_results else [],
        'export':candidates,
        'c1': Course.objects.all().distinct(),
        'show_results': show_results,
        'eng': eng,
        'poly': poly,
        'arts': arts,
        'iti': iti,
    }

def index(request):
    context = get_candidate_context(request)
    return render (request,"index.html", context)

def sample(request):
    return render(request, "sample.html")

@login_required
def rec(request):
    context = get_candidate_context(request)
    return render(request, 'recruiter_page.html', context)


import openpyxl
def export(request):
    context = get_candidate_context(request)
    candidates = context['export']
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Candidates"

    # Header row (in your desired order)
    ws.append([
        'S.No',
        'Name',
        'Course',
        'College',
        'Mobile Number',
        'Email',
        'Training Provider'
    ])

    # Data rows
    for i, c in enumerate(candidates, start=1):
        ws.append([
            i,
            c.name,
            str(c.course),
            str(c.college_name),
            c.mobile_number,
            c.email,
            str(c.tp),
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=candidates.xlsx'
    wb.save(response)
    return response
