from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/edit/<int:id>/', views.edit_employee, name='edit_employee'),
    path('employees/delete/<int:id>/', views.delete_employee, name='delete_employee'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/report/', views.attendance_report, name='attendance_report'),
    
    path('resume/screening/', views.resume_screening, name='resume_screening'),
    path("chatbot/", views.hr_assistant_view, name="hr_chatbot"),
     
    path("leave/apply/", views.apply_leave, name="apply_leave"),
    path("leave/my/", views.my_leave_requests, name="my_leave_requests"),
    path("leave/manage/", views.manage_leave_requests, name="manage_leave_requests"),
    path("leave/update/<int:leave_id>/<str:status>/", views.update_leave_status, name="update_leave_status"),
    
    

]
