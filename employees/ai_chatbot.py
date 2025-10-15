import logging
# DO NOT import pipeline at the top of the file. This is the key change.
# from transformers import pipeline 

# --- Configuration ---
MODEL_NAME = "distilbert-base-cased-distilled-squad"
CONFIDENCE_THRESHOLD = 0.30  # Don't return answers with confidence lower than 30%

# Setup logging
logger = logging.getLogger(__name__)

# --- The Knowledge Base ---
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

# --- Lazy Loading for the Model ---

# 1. Initialize the pipeline as 'None'. This uses almost no memory on startup.
qa_pipeline = None

def _initialize_pipeline():
    global qa_pipeline
    if qa_pipeline is not None:
        return

    try:
        # The import MUST be here
        from transformers import pipeline
        
        logger.info(f"Loading QA model...")
        qa_pipeline = pipeline("question-answering", model=MODEL_NAME)
        logger.info("✅ QA model loaded successfully.")
    except Exception as e:
        logger.error(f"⚠️ Could not load QA model: {e}")
        qa_pipeline = None

def _get_relevant_context(question):
    """
    A simple keyword-based retriever to find the best context for a question.
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
    
    return " ".join(KNOWLEDGE_BASE.values())


def ask_question(question: str) -> str:
    """
    Answers a question based on the internal knowledge base.
    """
    # 3. Check if the pipeline is loaded. If not, load it now.
    if qa_pipeline is None:
        _initialize_pipeline()
    
    # If initialization failed, qa_pipeline will still be None
    if not qa_pipeline:
        return "I'm sorry, but the AI Assistant is currently offline. Please try again later."

    logger.info(f"❓ Received question: {question}")
    
    context = _get_relevant_context(question)
    result = qa_pipeline(question=question, context=context)
    logger.info(f"🤖 AI Result: {result}")
    
    if result["score"] < CONFIDENCE_THRESHOLD:
        return "I'm sorry, but I'm not confident I have the right information for that question. Could you try rephrasing it?"
        
    return result["answer"].strip()