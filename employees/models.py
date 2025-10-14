from django.db import models
from users.models import CustomUser
from django.utils import timezone


class EmployeeProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # no default
    department = models.CharField(max_length=100, blank=True, null=True)
    salary = models.FloatField(default=0.0)
    performance_score = models.FloatField(default=0)

    def __str__(self):
        return self.user.username

class Attendance(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='attendance_records')  # no default
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.employee.user.username} - {self.date} - {self.status}"

class Payroll(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)  # no default
    month = models.CharField(max_length=20)
    base_salary = models.FloatField()
    bonus = models.FloatField(default=0)
    deductions = models.FloatField(default=0)

    def total_salary(self):
        return self.base_salary + self.bonus - self.deductions

    def __str__(self):
        return f"{self.employee.user.username} - {self.month}"



#Employee Leave manage

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="leave_requests")
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.employee.user.username} - {self.status} ({self.start_date} to {self.end_date})"
