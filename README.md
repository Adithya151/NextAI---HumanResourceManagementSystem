NEXTAI — AI-Driven HR Management System

NEXTAI is an intelligent HR automation web platform built with Django and AI-powered tools.
It streamlines attendance tracking, leave management, resume screening, and chatbot-based HR support — all in one modern portal.


🚀 Features

👥 Employee Management
    Admins and Managers can add, edit, and delete employees.
    Role-based dashboards (Admin / Manager / Recruiter / Employee).

⏰ Attendance System
    Employees can mark attendance with a single click.
    Admins can view complete attendance history.

📝 Leave Management
    Employees can apply for leave.
    Managers/Admins can approve or reject leave requests instantly.

🤖 AI Resume Screening
    Recruiters can upload resumes in PDF format.
    The integrated AI (HuggingFace model) analyzes resumes and scores candidates based on job relevance.

💬 HR Chatbot
    Smart AI chatbot answers HR-related queries instantly.
    Powered by NLP to provide policy and payroll responses.

🔒 Authentication & Security
    Only registered users can access dashboards.
    Unauthorized users are redirected to the login page.
    Secure login/logout system with success messages.


🛠️ Tech Stack

| Layer           | Technology                               |
| --------------- | ---------------------------------------- |
| **Frontend**    | HTML5, CSS3, JavaScript, Bootstrap       |
| **Backend**     | Django 5+, Python 3.12                   |
| **Database**    | MySQL (via Railway for cloud deployment) |
| **AI/ML**       | HuggingFace Transformers (DistilBERT)    |
| **Auth**        | Django Auth System                       |
| **Environment** | `.env` variables using `python-dotenv`   |


📂 Folder Structure

SmartHR/
├── Hrms/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── employees/
│   ├── templates/
│   │   ├── dashboards/
│   │   ├── leave/
│   │   └── hr_chatbot.html
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── ai_chatbot.py
│   └── utils.py
├── users/
│   ├── views.py
│   ├── templates/
│   │   └── login.html
├── manage.py
├── .env
├── .gitignore
└── README.md








