from app.calculator import compute_real_apr
from app.grounding import verify_clause_grounding

def test_apr_math():
    print("--- Running APR Math Calculation Checks ---")
    
    # Test case 1: Our standard demo loan terms
    # Principal: 5,00,000, Advertised interest: 10.0%, Tenure: 24 months,
    # Processing fee: 25,000, Upfront fee: 5,000, Monthly maintenance fee: 500
    res1 = compute_real_apr(
        loan_amount=500000.0,
        advertised_rate=10.0,
        tenure_months=24,
        processing_fee=25000.0,
        other_upfront_fees=5000.0,
        recurring_monthly_fees=500.0
    )
    print("Demo Loan Results:")
    print(f"  Base EMI: {res1['base_emi']} (Expected: 23072.46)")
    print(f"  Total Repayment (Advertised): {res1['total_repayment_advertised']} (Expected: ~553739.12)")
    print(f"  Total Repayment (Real): {res1['total_repayment_real']} (Expected: ~565739.12)")
    print(f"  Cost Difference: {res1['cost_difference']} (Expected: ~42000.0)")
    print(f"  Real APR: {res1['effective_apr']}% (Expected: ~18.48%)")
    
    assert abs(res1["effective_apr"] - 18.48) < 0.05, f"Failed: APR calculated as {res1['effective_apr']}"
    print("[PASS] Demo Loan APR Calculation is correct!")

    # Test case 2: 0% Interest Advertised Credit Card Loan with Upfront Fee
    # Principal: 1,00,000, Advertised interest: 0.0%, Tenure: 12 months,
    # Processing fee: 5,000, Upfront fee: 0, Monthly maintenance fee: 0
    res2 = compute_real_apr(
        loan_amount=100000.0,
        advertised_rate=0.0,
        tenure_months=12,
        processing_fee=5000.0,
        other_upfront_fees=0.0,
        recurring_monthly_fees=0.0
    )
    print("\n0% Advertised Loan Results:")
    print(f"  Base EMI: {res2['base_emi']} (Expected: 8333.33)")
    print(f"  Real APR: {res2['effective_apr']}% (Expected: ~9.59%)")
    
    # 95,000 disbursed, 12 payments of 8333.33. Monthly IRR is ~0.799%, annualized is ~9.59%
    assert abs(res2["effective_apr"] - 9.59) < 0.2, f"Failed: APR calculated as {res2['effective_apr']}"
    print("[PASS] 0% Advertised Loan APR Calculation is correct!")


def test_grounding_check():
    print("\n--- Running Grounding Check Checks ---")
    
    doc = """
    Interest on the credit facility shall accrue daily at the default rate of twenty-four percent (24.00%) per annum
    in the event of any default lasting longer than 5 days.
    """
    
    # Test valid substring
    clause_ok = "default rate of twenty-four percent (24.00%) per annum"
    res_ok = verify_clause_grounding(clause_ok, doc)
    print(f"  Matching: '{clause_ok[:35]}...' -> Grounded? {res_ok}")
    assert res_ok == True, "Failed: should have verified valid substring"
    
    # Test minor spacing/case mismatch
    clause_space = "Default  Rate of twenty-four percent  (24.00%)"
    res_space = verify_clause_grounding(clause_space, doc)
    print(f"  Matching: '{clause_space[:35]}...' -> Grounded? {res_space}")
    assert res_space == True, "Failed: spacing and case mismatch should be handled and grounded"
    
    # Test hallucinated phrase
    clause_bad = "interest rate will increase to thirty percent (30.00%)"
    res_bad = verify_clause_grounding(clause_bad, doc)
    print(f"  Matching: '{clause_bad[:35]}...' -> Grounded? {res_bad}")
    assert res_bad == False, "Failed: should have flagged hallucinated phrase"
    
    print("[PASS] Grounding verification checks passed!")

if __name__ == "__main__":
    test_apr_math()
    test_grounding_check()
    print("\n[SUCCESS] All unit tests passed!")
