from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from skillapp.models import CandidateProfile, Year, CollegeType, College, Department, Course, TrainingProvider
from django.http import HttpResponse

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


def my_home(request):
    selected = {
        'year': '',
        'college_type': '',
        'department': '',
        'course': '',
        'tp': '',
    }
    if request.method == 'POST':
        selected['year'] = request.POST.get('year', '')
        selected['college_type'] = request.POST.get('college_type', '')
        selected['department'] = request.POST.get('department', '')
        selected['course'] = request.POST.get('course', '')
        selected['tp'] = request.POST.get('tp', '')
        candidates = CandidateProfile.objects.all()
        if selected['year']:
            candidates = candidates.filter(year__name=selected['year'])
        if selected['college_type']:
            candidates = candidates.filter(college_type__type_name=selected['college_type'])
        if selected['department']:
            candidates = candidates.filter(department__dept_name=selected['department'])
        if selected['course']:
            candidates = candidates.filter(course__course_name=selected['course'])
        if selected['tp']:
            candidates = candidates.filter(tp__tp_name=selected['tp'])
        # Filter dropdown options based on filtered candidates
        years = Year.objects.filter(candidateprofile__in=candidates).distinct()
        college_types = CollegeType.objects.filter(candidateprofile__in=candidates).distinct()
        departments = Department.objects.filter(candidateprofile__in=candidates).distinct()
        courses = Course.objects.filter(candidateprofile__in=candidates).distinct()
        tps = TrainingProvider.objects.filter(candidateprofile__in=candidates).distinct()
        c1=Course.objects.all().distinct()
        context = {
            'years': years,
            'college_types': college_types,
            'departments': departments,
            'courses': courses,
            'tps': tps,
            'selected': selected,
            'candidate_count': candidates.count(),
            'candidates': candidates,
            'c1':c1,
        }
        return render(request, 'nm_skill.html', context)
    # Default page load - show all options
    context = {
        'years': Year.objects.all().distinct(),
        'college_types': CollegeType.objects.all().distinct(),
        'departments': Department.objects.all().distinct(),
        'courses': Course.objects.all().distinct(),
        'tps': TrainingProvider.objects.all().distinct(),
        'selected': selected,
        'candidate_count': 0,
        'candidates': [],
        'c1': Course.objects.all().distinct(),
        
    }
    return render(request, 'nm_skill.html', context)

@login_required
def rec(request):
    return render (request, "admin_dash.html")
