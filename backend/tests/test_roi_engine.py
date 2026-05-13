import pytest
from services.roi_engine import ROIInput, calculate_roi

def test_strong_deal():
    input = ROIInput(
        purchase_price=80000,
        rehab_cost=30000,
        arv=160000,
        monthly_taxes=150,
        monthly_insurance=100,
        rehab_duration_months=4
    )
    result = calculate_roi(input)
    assert result.roi_percentage > 20
    assert result.is_good_deal == True
    assert "Strong" in result.verdict

def test_bad_deal():
    input = ROIInput(
        purchase_price=140000,
        rehab_cost=40000,
        arv=160000,
        monthly_taxes=200,
        monthly_insurance=150,
        rehab_duration_months=6
    )
    result = calculate_roi(input)
    assert result.roi_percentage < 0
    assert result.is_good_deal == False
    assert "lose money" in result.verdict

def test_breakeven_deal():
    input = ROIInput(
        purchase_price=100000,
        rehab_cost=20000,
        arv=125000,
        monthly_taxes=150,
        monthly_insurance=100,
        rehab_duration_months=3
    )
    result = calculate_roi(input)
    assert result.roi_percentage < 5
    assert result.is_good_deal == False

def test_seventy_percent_rule():
    arv = 200000
    rehab = 30000
    input = ROIInput(
        purchase_price=100000,
        rehab_cost=rehab,
        arv=arv,
        monthly_taxes=150,
        monthly_insurance=100,
        rehab_duration_months=4
    )
    result = calculate_roi(input)
    expected_max = (arv * 0.70) - rehab
    assert round(result.seventy_percent_max, 2) == round(expected_max, 2)

def test_luxury_market():
    input = ROIInput(
        purchase_price=500000,
        rehab_cost=150000,
        arv=850000,
        monthly_taxes=800,
        monthly_insurance=400,
        rehab_duration_months=8
    )
    result = calculate_roi(input)
    assert result.net_profit > 0
    assert result.roi_percentage > 0