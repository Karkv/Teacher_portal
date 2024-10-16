from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.teacher_dashboard, name='teacher_dashboard'),  # Main dashboard view
    path('api/schedule/', views.get_teacher_schedule, name='get_teacher_schedule'),  # API for calendar events
    path('create_subject/', views.create_subject, name='create_subject'),
    path('accounts/', include('django.contrib.auth.urls')),  # For built-in login/logout views
    path('create_event/', views.create_event, name='create_event'),

    path('create_holiday/', views.create_holiday, name='create_holiday'),
    path('login/', views.login_view, name='login_view'),  # Custom login view
    path('logout/', views.logout_view, name='logout_view'),  # Logout view
]
