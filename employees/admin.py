from django.contrib import admin
from .models import EmployeeProfile, Attendance, Payroll
'''
admin.site.register(EmployeeProfile)
admin.site.register(Attendance)
admin.site.register(Payroll)
'''

from django.contrib import admin
from .models import EmployeeProfile, Attendance, Payroll
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser

# EmployeeProfile admin
@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'salary', 'performance_score')  # Columns to show
    search_fields = ('user__username', 'department')  # Search by username or department
    list_filter = ('department',)  # Filter by department

# Attendance admin
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status')
    search_fields = ('employee__user__username',)
    list_filter = ('status', 'date')

# Payroll admin
@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'base_salary', 'bonus', 'deductions', 'total_salary')
    search_fields = ('employee__user__username',)

