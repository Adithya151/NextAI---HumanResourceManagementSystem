from django import forms
from .models import EmployeeProfile

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['department', 'salary']

class ResumeUploadForm(forms.Form):
    resume = forms.FileField()


from .models import LeaveRequest

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ["start_date", "end_date", "reason"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "reason": forms.Textarea(attrs={"rows": 3}),
        }