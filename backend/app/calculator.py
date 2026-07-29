def compute_real_apr(
    loan_amount: float,
    advertised_rate: float,
    tenure_months: int,
    processing_fee: float,
    other_upfront_fees: float,
    recurring_monthly_fees: float
) -> dict:
    """
    Computes the nominal and effective APR, total repayments, and cost difference.
    Also returns fields for the visual Cost Breakdown Graphic.
    """
    # 1. Calculate standard EMI based on advertised rate
    r_advertised_monthly = (advertised_rate / 12) / 100
    
    if r_advertised_monthly == 0:
        base_emi = loan_amount / tenure_months
    else:
        num = loan_amount * r_advertised_monthly * ((1 + r_advertised_monthly) ** tenure_months)
        den = ((1 + r_advertised_monthly) ** tenure_months) - 1
        base_emi = num / den
        
    total_repayment_advertised = base_emi * tenure_months
    
    # 2. Calculate actual cash flows
    net_disbursement = loan_amount - processing_fee - other_upfront_fees
    real_monthly_repayment = base_emi + recurring_monthly_fees
    total_repayment_real = real_monthly_repayment * tenure_months
    
    # Cost components for visual breakdown graphic
    borrow_amount = loan_amount
    interest_amount = total_repayment_advertised - loan_amount
    extra_charges = processing_fee + other_upfront_fees + (recurring_monthly_fees * tenure_months)
    total_estimated = borrow_amount + interest_amount + extra_charges
    
    cost_difference = total_estimated - total_repayment_advertised
    
    # 3. Solve for monthly IRR using Bisection Method
    if net_disbursement >= total_repayment_real or net_disbursement <= 0:
        return {
            "base_emi": round(base_emi, 2),
            "effective_apr": round(advertised_rate, 2),
            "total_repayment_advertised": round(total_repayment_advertised, 2),
            "total_repayment_real": round(total_repayment_real, 2),
            "cost_difference": round(cost_difference, 2),
            "borrow_amount": round(borrow_amount, 2),
            "interest_amount": round(interest_amount, 2),
            "extra_charges": round(extra_charges, 2),
            "total_estimated": round(total_estimated, 2)
        }
        
    low = 0.0
    high = 2.0
    
    for _ in range(60):
        mid = (low + high) / 2
        if mid == 0:
            pv = real_monthly_repayment * tenure_months
        else:
            pv = real_monthly_repayment * (1 - (1 + mid) ** -tenure_months) / mid
            
        if pv > net_disbursement:
            low = mid
        else:
            high = mid
            
    nominal_apr_percent = low * 12 * 100
    
    return {
        "base_emi": round(base_emi, 2),
        "effective_apr": round(nominal_apr_percent, 2),
        "total_repayment_advertised": round(total_repayment_advertised, 2),
        "total_repayment_real": round(total_repayment_real, 2),
        "cost_difference": round(cost_difference, 2),
        "borrow_amount": round(borrow_amount, 2),
        "interest_amount": round(interest_amount, 2),
        "extra_charges": round(extra_charges, 2),
        "total_estimated": round(total_estimated, 2)
    }
