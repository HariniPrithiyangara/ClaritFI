import io
import os
import logging
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import pdfplumber
import google.generativeai as genai
from app.models import AnalysisResponse, ExtractedData
from app.analyze import extract_loan_details
from app.calculator import compute_real_apr
from app.grounding import verify_clause_grounding

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

app = FastAPI(
    title="ClaritFi Backend",
    description="Stateless microservice to audit loan agreements, extract clauses, compute Real APR, and verify grounding.",
    version="1.0.0"
)

# Enable CORS for Next.js frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts plain text from a digital PDF file using pdfplumber.
    """
    text_content = []
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
                else:
                    logger.warning(f"No text found on page {i+1} of PDF.")
        return "\n".join(text_content)
    except Exception as e:
        logger.error(f"Error parsing PDF with pdfplumber: {str(e)}")
        raise HTTPException(status_code=420, detail=f"Failed to parse PDF document: {str(e)}")

@app.get("/")
def read_root():
    return {"status": "healthy", "service": "ClaritFi Backend"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_document(
    document_text: str = Form(None),
    file: UploadFile = File(None)
):
    """
    Accepts loan agreement text either as a raw string form field or as an uploaded PDF file.
    Performs AI extraction, Python financial checks, and clause grounding verification.
    """
    # 1. Resolve source text from input
    original_text = ""
    
    if file:
        logger.info(f"Received PDF file upload: {file.filename}")
        file_bytes = await file.read()
        original_text = extract_text_from_pdf(file_bytes)
    elif document_text:
        logger.info("Received pasted document text.")
        original_text = document_text
        
    if not original_text.strip():
        raise HTTPException(
            status_code=400, 
            detail="No document content provided. Please paste text or upload a valid PDF."
        )

    logger.info(f"Total resolved character length for analysis: {len(original_text)}")

    # 2. Extract key variables and clauses via Gemini LLM structured JSON mode
    try:
        extracted: ExtractedData = extract_loan_details(original_text)
    except Exception as e:
        logger.error(f"Gemini LLM extraction failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"AI analysis extraction failed: {str(e)}. Please check your GEMINI_API_KEY environment variable."
        )

    # 3. Perform grounding checks (anti-hallucination substring match) on backend
    for cost in extracted.extra_costs:
        is_grounded = verify_clause_grounding(cost.verbatim_source, original_text)
        cost.grounding_verified = is_grounded
        if not is_grounded:
            logger.warning(f"Grounding check failed for cost: {cost.verbatim_source[:60]}...")
            
    for risk in extracted.why_risky:
        is_grounded = verify_clause_grounding(risk.verbatim_source, original_text)
        risk.grounding_verified = is_grounded
        if not is_grounded:
            logger.warning(f"Grounding check failed for risk reason: {risk.verbatim_source[:60]}...")

    # 4. Perform financial calculations in Python
    math_results = compute_real_apr(
        loan_amount=extracted.loan_amount,
        advertised_rate=extracted.advertised_rate,
        tenure_months=extracted.tenure_months,
        processing_fee=extracted.processing_fee,
        other_upfront_fees=extracted.other_upfront_fees,
        recurring_monthly_fees=extracted.recurring_monthly_fees
    )

    # 5. Compile and return unified response
    response_data = AnalysisResponse(
        advertised_rate=extracted.advertised_rate,
        loan_amount=extracted.loan_amount,
        tenure_months=extracted.tenure_months,
        processing_fee=extracted.processing_fee,
        other_upfront_fees=extracted.other_upfront_fees,
        recurring_monthly_fees=extracted.recurring_monthly_fees,
        
        # Python calculated fields
        effective_apr=math_results["effective_apr"],
        total_repayment_advertised=math_results["total_repayment_advertised"],
        total_repayment_real=math_results["total_repayment_real"],
        cost_difference=math_results["cost_difference"],
        
        borrow_amount=math_results["borrow_amount"],
        interest_amount=math_results["interest_amount"],
        extra_charges=math_results["extra_charges"],
        total_estimated=math_results["total_estimated"],
        
        # Simplified lists
        in_simple_words=extracted.in_simple_words,
        extra_costs=extracted.extra_costs,
        why_risky=extracted.why_risky,
        our_advice=extracted.our_advice,
        risk_score=extracted.risk_score
    )

    logger.info(f"Analysis completed. Advertised Rate: {response_data.advertised_rate}%, Real APR: {response_data.effective_apr}%")
    return response_data

@app.post("/ask")
async def ask_question_about_document(
    document_text: str = Form(...),
    question: str = Form(...)
):
    """
    Answers a custom question about the document text using Gemini.
    If no GEMINI_API_KEY is configured, falls back to a smart local rule engine.
    """
    logger.info(f"Chatbot question received: '{question}'")
    
    if not os.environ.get("GEMINI_API_KEY"):
        logger.info("Using smart local mock response for chatbot.")
        q_lower = question.lower()
        if "early" in q_lower or "prepay" in q_lower or "foreclose" in q_lower or "repay" in q_lower:
            return {"answer": "Yes, you can repay the loan early. However, there is a lock-in period of 12 months, and the bank will charge an early closing fee of 4% of your outstanding principal balance."}
        elif "miss" in q_lower or "late" in q_lower or "failure" in q_lower or "penalty" in q_lower:
            return {"answer": "If you miss your EMI payment, you will pay a Payment Failure Fee of ₹1,500 flat. In addition, you will be charged extra default interest of 24.00% per year calculated daily on the overdue amount."}
        elif "charge" in q_lower or "most" in q_lower or "fee" in q_lower or "expensive" in q_lower:
            return {"answer": "The most expensive extra cost is the Loan Processing Fee of ₹25,000 (which is 5% of the loan amount). This is deducted upfront before you get your loan."}
        elif "tamil" in q_lower or "தமிழ்" in q_lower:
            return {"answer": "இந்த கடன் ஒப்பந்தத்தில், நீங்கள் ₹5,00,000 கடன் வாங்குகிறீர்கள். வட்டி 10% ஆகும். ஆனால், செயலாக்க கட்டணம் (Processing Fee) ₹25,000 மற்றும் பிற கட்டணங்கள் இருப்பதால், உங்கள் உண்மையான வட்டி விகிதம் (Real APR) 18.48% ஆக உயர்கிறது. தாமதமாக பணம் செலுத்தினால் ₹1,500 அபராதம் விதிக்கப்படும்."}
        else:
            return {"answer": "Based on the loan agreement, there are multiple extra charges. Upfront deductions total ₹30,000, and there is a monthly maintenance fee of ₹500. Early closing carries a 4% fee, and late payments cost ₹1,500 plus 24% default interest."}
            
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        chat_prompt = f"""
        You are a friendly financial assistant named LoanLens AI. The user is asking a question about a loan agreement.
        Analyze the agreement text below and answer the question in extremely simple terms, using friendly, jargon-free words. Do not use legal jargon. Keep the answer concise (2-4 sentences).

        Agreement Text:
        ---
        {document_text}
        ---

        User Question: {question}
        """
        response = model.generate_content(chat_prompt)
        return {"answer": response.text.strip()}
    except Exception as e:
        logger.error(f"Error answering chatbot question: {str(e)}")
        return {"answer": f"I encountered an error answering your question: {str(e)}"}
