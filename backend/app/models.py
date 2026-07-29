from pydantic import BaseModel, Field
from typing import List

class ExtraCostItem(BaseModel):
    name: str = Field(description="The friendly, simplified name of the charge (e.g., 'Loan Processing Fee', 'Payment Failure Fee', 'Early Closing Fee', 'Paperwork charges', 'Late Payment Interest'). Do NOT use complex legal/financial jargon like 'Foreclosure charges', 'Penal interest', 'Documentation fee', or 'Processing fee' directly without simplifying them.")
    amount: str = Field(description="The cost amount, e.g., '₹10,000', '3%', '₹1,500'.")
    description: str = Field(description="A short, friendly explanation of what this fee is, using simple terms.")
    verbatim_source: str = Field(description="The exact verbatim sentence or clause from the document where this cost is mentioned.")
    grounding_verified: bool = Field(description="Whether the verbatim text matches the original document.")

class RiskReason(BaseModel):
    reason: str = Field(description="A bullet point explaining a risk or cost flag in simple terms, e.g., 'High processing fee', 'Expensive late penalty', 'Charges for closing loan early'.")
    verbatim_source: str = Field(description="The exact verbatim sentence or clause from the document relating to this risk.")
    severity: str = Field(description="The severity rating of this risk, must be exactly one of: 'HIGH', 'MEDIUM', 'LOW'. Use 'HIGH' for severe upfront charges, high interest penalties, or early repayment lock-in/fees. Use 'MEDIUM' for moderate fees/penalties. Use 'LOW' for standard terms or minor conditions.")
    grounding_verified: bool = Field(description="Whether the verbatim text matches the original document.")

class ExtractedData(BaseModel):
    advertised_rate: float = Field(description="The advertised interest rate percentage (e.g., 10.0 for 10%).")
    loan_amount: float = Field(description="The principal loan or credit limit amount.")
    tenure_months: int = Field(description="The tenure of the loan in months.")
    
    # Financial components for the breakdown
    processing_fee: float = Field(description="The upfront processing fee amount. Extract 0.0 if none.")
    other_upfront_fees: float = Field(description="Other upfront fees like document, administrative, or insurance charges. Extract 0.0 if none.")
    recurring_monthly_fees: float = Field(description="Ongoing monthly maintenance or account fees. Extract 0.0 if none.")
    
    in_simple_words: List[str] = Field(description="A list of 4-6 bullet points explaining the loan in extremely simple terms, with no legal words. Format: ['You are borrowing ₹X.', 'The bank charges Y% interest.', 'Besides interest, there are extra fees.']")
    extra_costs: List[ExtraCostItem] = Field(description="List of all upfront and penalty costs simplified for the user.")
    why_risky: List[RiskReason] = Field(description="List of 3-5 specific reasons why this loan is risky or contains hidden costs.")
    our_advice: List[str] = Field(description="List of 3-5 actionable recommendations for the borrower (e.g., 'Compare with another lender', 'Ask if the processing fee can be reduced').")
    risk_score: float = Field(description="A risk score from 1.0 (very safe) to 10.0 (high fees/penalties/risks).")

class AnalysisResponse(BaseModel):
    advertised_rate: float
    loan_amount: float
    tenure_months: int
    processing_fee: float
    other_upfront_fees: float
    recurring_monthly_fees: float
    
    # Python-calculated math parameters
    effective_apr: float
    total_repayment_advertised: float
    total_repayment_real: float
    cost_difference: float
    
    # Cost Breakdown Graphic structure
    borrow_amount: float
    interest_amount: float
    extra_charges: float
    total_estimated: float
    
    # Friendly descriptions and advice
    in_simple_words: List[str]
    extra_costs: List[ExtraCostItem]
    why_risky: List[RiskReason]
    our_advice: List[str]
    risk_score: float
