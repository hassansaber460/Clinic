from django.urls import path
from . import views

urlpatterns = [
    path('register_medical_staff/', views.register_medical_staff, name='registerMedicalStaff'),
    path('register_assistant_staff/', views.register_assistant_staff, name='register_assistant_staff'),
    path('base/', views.loadBase),
    path('add_schedule/', views.add_schedule, name='add_schedule'),
    path('show_schedule/', views.show_schedule, name='show_schedule'),
    path('schedule_update/<int:schedule_id>/', views.schedule_update, name='schedule_update'),
    path('schedule_delete/<int:schedule_id>/', views.schedule_delete, name='schedule_delete')

]
