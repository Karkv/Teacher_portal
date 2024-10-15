from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Teacher, Schedule, Subject, Holiday
import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import datetime

# Teacher Dashboard with Subject Performance Overview
@login_required
def teacher_dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    subjects = teacher.subjects.all()

    # Handle subject selection
    selected_subject_id = request.GET.get('subject')
    selected_subject = None

    performance_data = []
    for subject in subjects:
        total_hours = subject.total_hours
        completed_minutes = sum(
            schedule.duration_minutes for schedule in Schedule.objects.filter(teacher=teacher, subject=subject)
        )
        completed_hours = completed_minutes / 60
        remaining_hours = max(total_hours - completed_hours, 0)

        data = {
            'subject': subject.name,
            'total_hours': total_hours,
            'completed_hours': round(completed_hours, 2),
            'remaining_hours': round(remaining_hours, 2),
        }
        performance_data.append(data)

        if str(subject.id) == selected_subject_id:
            selected_subject = data

    context = {
        'teacher': teacher,
        'performance_data': performance_data,
        'selected_subject': selected_subject,
        'subjects': subjects,
    }
    return render(request, 'schedules/dashboard.html', context)

# Create Holiday
@login_required
def create_holiday(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        Holiday.objects.create(name=name, date=date)
        return redirect('teacher_dashboard')

    return render(request, 'schedules/create_holiday.html')

# Fetch Teacher Schedule and Holidays for FullCalendar
import holidays  # Import the holidays library

@login_required
def get_teacher_schedule(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    schedules = Schedule.objects.filter(teacher=teacher)

    # Prepare schedule events (class events)
    events = [
        {
            'title': f"{schedule.subject.name} - {schedule.duration_minutes} min",
            'start': schedule.start_time.isoformat(),
            'end': (schedule.start_time + pd.Timedelta(minutes=schedule.duration_minutes)).isoformat(),
            'type': 'class',
            'subject': schedule.subject.name,  # Pass subject name for coloring
        } for schedule in schedules
    ]

    # Add built-in holidays from the holidays library (e.g., India holidays)
    india_holidays = holidays.India(years=202)  # Add year dynamically if needed
    for date, name in india_holidays.items():
        events.append({
            'title': name,
            'start': date.isoformat(),
            'allDay': True,
            'type': 'holiday',  # Mark it as a holiday
        })

    # Add custom holidays created by teachers
    custom_holidays = Holiday.objects.all()
    for holiday in custom_holidays:
        events.append({
            'title': holiday.name,
            'start': holiday.date.isoformat(),
            'allDay': True,
            'type': 'holiday',  # Mark it as a holiday
        })

    return JsonResponse(events, safe=False)


# Create Subject with Start Date

@login_required
def create_subject(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        total_hours = float(request.POST.get('total_hours'))
        start_date_str = request.POST.get('start_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()  # Parse start date

        teacher = get_object_or_404(Teacher, user=request.user)

        # Create the new subject
        subject = Subject.objects.create(
            name=name, total_hours=total_hours, start_date=start_date
        )
        
        # Add the subject to the teacher's subjects list
        teacher.subjects.add(subject)

        return redirect('teacher_dashboard')

    return render(request, 'schedules/create_subject.html')


# Login and Logout Views
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('teacher_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'schedules/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')