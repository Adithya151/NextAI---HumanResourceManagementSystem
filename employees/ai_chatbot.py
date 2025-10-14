from transformers import pipeline
'''
try:
    qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
except Exception as e:
    print("⚠️ Could not load model:", e)
    qa_pipeline = None

def ask_question(question, context="Our HR policy: employees get 20 annual leave days, salaries are paid on the 28th of every month, and attendance must be marked daily."):
    if qa_pipeline:
        print("✅ Processing:", question)  # Debug log
        result = qa_pipeline(question=question, context=context)
        print("🤖 Bot result:", result)    # Debug log
        return result["answer"]
    return "Sorry, the chatbot is not available right now."
 
    
from transformers import pipeline

chatbot = pipeline("text-generation", model="distilgpt2")

def ask_question(question):
    result = chatbot(question, max_length=50, num_return_sequences=1)
    return result[0]["generated_text"]
'''


import logging
from transformers import pipeline

# --- Configuration ---
MODEL_NAME = "distilbert-base-cased-distilled-squad"
CONFIDENCE_THRESHOLD = 0.30  # Don't return answers with confidence lower than 30%

# Setup logging
logger = logging.getLogger(__name__)

# --- The Knowledge Base ---
# In a real application, this would come from a database, text files, or a wiki.
# This structure allows the bot to handle different topics.
KNOWLEDGE_BASE = {
    "leave_policy": """
        Our company's official leave policy states that all full-time employees are entitled to 20 days of annual paid leave. 
        Sick leave is granted for up to 10 days per year with a doctor's note. 
        Maternity leave is 12 weeks, and paternity leave is 2 weeks. 
        All leave requests must be submitted through the HRMS portal at least one week in advance for annual leave.
    """,
    "payroll_information": """
        Salaries are processed on the 25th of each month and are paid out on the 28th. 
        Payslips are available for download in the HRMS portal on the 27th. 
        For any payroll discrepancies, please contact the HR department by emailing hr@company.com.
        Bonuses are typically paid out in the December payroll cycle.
    """,
    "attendance_policy": """
        Employees are expected to mark their attendance daily through the HRMS portal upon starting their workday. 
        The standard work hours are from 9:00 AM to 5:30 PM, with a 30-minute lunch break. 
        Remote employees must also mark their attendance online.
        Failure to mark attendance for three consecutive days without notification may be considered an unauthorized absence.
    """,
    "expense_reports": """
        To submit an expense report, employees must use the 'Expenses' section of the HRMS portal. 
        All claims must be accompanied by a valid digital receipt. 
        Reimbursements for approved expenses are processed within 5 business days and are paid with the next salary cycle.
    """
}

# --- Model Loading (Singleton Pattern) ---
# This loads the model only once when the Django server starts, which is highly efficient.
try:
    logger.info(f"Loading QA model: {MODEL_NAME}...")
    qa_pipeline = pipeline("question-answering", model=MODEL_NAME)
    logger.info("✅ QA model loaded successfully.")
except Exception as e:
    logger.error(f"⚠️ Could not load QA model: {e}")
    qa_pipeline = None

def _get_relevant_context(question):
    """
    A simple keyword-based retriever to find the best context for a question.
    In a more advanced system, this would be a more sophisticated search/embedding model.
    """
    question_lower = question.lower()
    if any(word in question_lower for word in ["leave", "vacation", "sick", "holiday"]):
        return KNOWLEDGE_BASE["leave_policy"]
    if any(word in question_lower for word in ["salary", "pay", "payslip", "paid"]):
        return KNOWLEDGE_BASE["payroll_information"]
    if any(word in question_lower for word in ["attendance", "present", "timing", "hours"]):
        return KNOWLEDGE_BASE["attendance_policy"]
    if any(word in question_lower for word in ["expense", "reimbursement", "receipt"]):
        return KNOWLEDGE_BASE["expense_reports"]
    
    # Fallback to a general context if no specific keywords are found
    return " ".join(KNOWLEDGE_BASE.values())


def ask_question(question: str) -> str:
    """
    Answers a question based on the internal knowledge base.
    """
    if not qa_pipeline:
        return "I'm sorry, but the AI Assistant is currently offline. Please try again later."

    logger.info(f"❓ Received question: {question}")
    
    # 1. Retrieve the most relevant context
    context = _get_relevant_context(question)
    
    # 2. Get the answer from the model
    result = qa_pipeline(question=question, context=context)
    logger.info(f"🤖 AI Result: {result}")
    
    # 3. Check if the model is confident enough in its answer
    if result["score"] < CONFIDENCE_THRESHOLD:
        return "I'm sorry, but I'm not confident I have the right information for that question. Could you try rephrasing it?"
        
    return result["answer"].strip()
