from django.utils.timezone import now
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import EmployeeProfile, Attendance, Payroll
from .forms import EmployeeForm, ResumeUploadForm
from .utils import extract_text_from_pdf
from .ai import analyze_resume
from datetime import date  
from django.contrib import messages
from .ai_chatbot import ask_question
import json
# -------------------
# Role-based decorator
# -------------------
def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("🚫 You do not have permission to view this page.")
        return wrapper
    return decorator


# -------------------
# HOME + DASHBOARD
# -------------------
def home(request):
    return render(request, 'home.html')
from .models import EmployeeProfile, LeaveRequest

@login_required
def dashboard(request):
    role = request.user.role

    if role == 'Admin':
        # show all pending leave requests
        pending_leaves = LeaveRequest.objects.filter(status="Pending")[:5]
        return render(request, 'employees/dashboards/admin_dash.html', {
            "pending_leaves": pending_leaves
        })

    elif role == 'Manager':
        # show only pending requests for manager’s department/team (basic: all pending)
        pending_leaves = LeaveRequest.objects.filter(status="Pending")[:5]
        return render(request, 'employees/dashboards/manager_dash.html', {
            "pending_leaves": pending_leaves
        })

    elif role == 'Recruiter':
        return render(request, 'employees/dashboards/recruiter_dash.html')

    else:  # Employee
        try:
            profile = EmployeeProfile.objects.get(user=request.user)
            return render(request, 'employees/dashboards/employee_dash.html', {
                "profile": profile
            })
        except EmployeeProfile.DoesNotExist:
            return redirect('employee_list')


# -------------------
# EMPLOYEE MANAGEMENT
# -------------------
@login_required
@role_required(['Admin', 'Manager'])
def employee_list(request):
    employees = EmployeeProfile.objects.all()
    return render(request, "employees/employee_list.html", {"employees": employees})

@login_required
@role_required(['Admin', 'Manager'])
def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("employee_list")
    else:
        form = EmployeeForm()
    return render(request, "employees/employee_form.html", {"form": form})

@login_required
@role_required(['Admin', 'Manager'])
def edit_employee(request, id):
    emp = get_object_or_404(EmployeeProfile, id=id)
    form = EmployeeForm(request.POST or None, instance=emp)
    if form.is_valid():
        form.save()
        return redirect("employee_list")
    return render(request, "employees/employee_form.html", {"form": form})

@login_required
@role_required(['Admin'])
def delete_employee(request, id):
    emp = get_object_or_404(EmployeeProfile, id=id)
    # Decide if you also want to delete CustomUser here
    # emp.user.delete()
    emp.delete()
    return redirect("employee_list")


# -------------------
# ATTENDANCE
# -------------------
@login_required
@role_required(['Employee'])
def mark_attendance(request):
    if request.user.role != "Employee":
        return HttpResponseForbidden("Only employees can mark attendance.")

    emp_profile = EmployeeProfile.objects.get(user=request.user)
    today = now().date()

    # Check if already marked
    already_marked = Attendance.objects.filter(employee=emp_profile, date=today).exists()

    if not already_marked:
        Attendance.objects.create(employee=emp_profile, status="Present")
        status_message = "✅ Attendance marked successfully for today!"
    else:
        status_message = "⚠️ You have already marked attendance today."

    # Render to the new confirmation page
    return render(request, "employees/attendance_mark.html", {"message": status_message})

        

@login_required
def attendance_report(request):
    if request.user.role in ['Admin', 'Manager']:
        records = Attendance.objects.select_related('employee','employee__user').all().order_by('-date')
    else:
        emp_pro = EmployeeProfile.objects.get(user=request.user)
        records = Attendance.objects.filter(employee=emp_pro).order_by('-date') 
    return render(request, "employees/attendance_report.html", {"records": records})



# -------------------
# AI RESUME SCREENING
# -------------------
# In your views.py
import json # Make sure json is imported

@login_required
@role_required(['Recruiter'])
def resume_screening(request):
    if request.method == 'POST':
        resume_file = request.FILES.get('resume')
        job_description = request.POST.get('job_description')
        
        if not resume_file or not job_description:
            return render(request, 'employees/resume_screening.html', {'error': 'Both a resume and job description are required.'})

        try:
            print("--- Step 1: Extracting text from PDF ---")
            resume_text = extract_text_from_pdf(resume_file)
            # Let's print the first 500 characters to confirm it worked
            print(f"Resume Text (first 500 chars): {resume_text[:500]}")
            
            
            ai_response_dict = analyze_resume(
            resume_text=resume_text, 
            job_description=job_description
            )

            # THIS IS THE MOST IMPORTANT PRINT STATEMENT
            print(f"\n--- Step 3: Raw AI Response ---")
            print(f"Response from analyze_resume: {ai_response_dict}")
            print(f"Type of response: {type(ai_response_dict)}")
            
            analysis_result = None
            if isinstance(ai_response_dict, dict):
                analysis_result = ai_response_dict
            elif isinstance(ai_response_dict, str) and ai_response_dict.strip():
                # Added check to ensure string is not empty
                try:
                    analysis_result = json.loads(ai_response_dict)
                except json.JSONDecodeError:
                    print("!!! JSON DECODE ERROR: AI returned a string that is not valid JSON.")
                    raise ValueError("AI response was a malformed string.")
            else:
                raise TypeError("AI response is not in a valid format (dictionary or non-empty JSON string).")

            print("\n--- Step 4: Final analysis_result before rendering ---")
            print(f"Final context['result']: {analysis_result}")
            
            context = {'result': analysis_result}
            return render(request, 'employees/resume_screening.html', context)

        except Exception as e:
            # THIS IS THE SECOND MOST IMPORTANT PRINT STATEMENT
            print(f"\n!!! --- An Exception was caught! --- !!!")
            print(f"Error Type: {type(e)}")
            print(f"Error Message: {e}")
            
            context = {'error': f'An unexpected error occurred. Please check the logs.'}
            return render(request, 'employees/resume_screening.html', context)
            
    return render(request, 'employees/resume_screening.html')

# Don't forget your helper functions
# def extract_text_from_pdf(pdf_file): ...
# def analyze_resume(prompt): ...

@login_required
@role_required(['Employee', 'Recruiter'])
def hr_assistant_view(request):
    context = {}
    if request.method == 'POST':
        question = request.POST.get('question', '').strip()
        if question:
            # Call the corrected and improved function
            answer = ask_question(question)
            
            context['question'] = question
            context['answer'] = answer
            
    return render(request, 'employees/hr_chatbot.html', context)




from .models import LeaveRequest
from .forms import LeaveRequestForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Employee: Apply for leave
@login_required
@role_required(["Employee"])
def apply_leave(request):
    if request.method == "POST":
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = EmployeeProfile.objects.get(user=request.user)
            leave.save()
            return redirect("my_leave_requests")
    else:
        form = LeaveRequestForm()
    return render(request, "employees/leave/apply_leave.html", {"form": form})


# Employee: View own leave requests
@login_required
@role_required(["Employee"])
def my_leave_requests(request):
    leaves = LeaveRequest.objects.filter(employee__user=request.user).order_by("-created_at")
    return render(request, "employees/leave/my_leave_requests.html", {"leaves": leaves})


# Manager/Admin: Approve/Reject leave
@login_required
@role_required(["Admin", "Manager"])
def manage_leave_requests(request):
    leaves = LeaveRequest.objects.filter(status="Pending").order_by("-created_at")
    return render(request, "employees/leave/manage_leave_requests.html", {"leaves": leaves})


@login_required
@role_required(["Admin", "Manager"])
def update_leave_status(request, leave_id, status):
    # Only Admin/Manager can approve/reject
    if request.user.role not in ["Admin", "Manager"]:
        return HttpResponseForbidden("You cannot perform this action.")

    leave = get_object_or_404(LeaveRequest, id=leave_id)

    if status in ["Approved", "Rejected"]:
        leave.status = status
        leave.save()

    return redirect("manage_leave_requests") 

@login_required
@role_required(["Admin", "Manager"])
def manage_leave_requests(request):
    leaves = LeaveRequest.objects.filter(status="Pending").order_by("-created_at")
    return render(request, "employees/leave/manage_leave_requests.html", {"leaves": leaves})

