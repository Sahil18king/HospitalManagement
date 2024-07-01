from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", views.signup,name='signup'),
    path('loginform',views.loginform,name='loginform'),
    path('logout/', views.logout_view, name='logout'),
    path('add_staff_view/', views.add_staff_view, name='add_staff_view'),
    path('appointment/', views.appointment, name='appointment'),
    # path('view_profile/', views.view_profile, name='view_profile'),  # New URL pattern
    path('view_profile/<str:staff_type>/', views.view_profile, name='view_profile'),  # Updated URL pattern with staff_type parameter
    path('password_reset/', auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    # path('create-password/<uidb64>/<token>/', views.create_password, name='create_password'),
    #  path('get-doctors-by-department/', views.get_doctors_by_department, name='get_doctors_by_department'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('get-doctors/', views.get_doctors_by_department, name='get_doctors_by_department'),
    path('appointment/', views.appointment, name='appointment'),
    path('view_appointments/', views.view_appointments, name='view_appointments'),
    path('update_staff_details/', views.update_staff_details, name='update_staff_details'),
    path('get_available_time_slots/', views.get_available_time_slots, name='get_available_time_slots'),
    path('patient_details/', views.patient_details, name='patient_details'),
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('update_medicine/<int:medicine_id>/', views.update_medicine, name='update_medicine'),
    # path('view_patient_profile/<str:email>/', views.view_patient_profile, name='view_patient_profile'),
    path('view_patient_profile/<str:email>/<int:appointment_id>/', views.view_patient_profile, name='view_patient_profile'),
    path('previous_appointments/<str:email>/', views.previous_appointments, name='previous_appointments'),
    path('appointments/mark_done/', views.mark_appointment_done, name='mark_appointment_done'),
    path('appointments/history/', views.view_appointment_history, name='view_appointment_history'),
    path('medication_report/', views.medication_report, name='medication_report'),
    path('medication_report_pdf/', views.medication_report_pdf, name='medication_report_pdf'),
    path('add_room/', views.add_room, name='add_room'),
    # path('medication_report/', medication_report, name='medication_report'),
    
    # path('save_slots_for_doctor/', views.save_slots_for_doctor, name='save_slots_for_doctor'),
    # path('get-doctor-schedule/', views.get_doctor_schedule, name='get_doctor_schedule'),
    # path('get_slots_by_doctor/', views.get_slots_by_doctor, name='get_slots_by_doctor'),  
    
]
