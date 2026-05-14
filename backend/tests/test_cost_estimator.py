from services.cost_estimator import estimate_room_cost, estimate_total_rehab_cost

def test_c1_kitchen_no_cost():
    result = estimate_room_cost("kitchen", "C1")
    assert result["low_estimate"] == 0
    assert result["high_estimate"] == 0

def test_c5_kitchen_high_cost():
    result = estimate_room_cost("kitchen", "C5")
    assert result["low_estimate"] >= 40000
    assert result["high_estimate"] >= 40000

def test_midpoint_calculation():
    result = estimate_room_cost("bathroom", "C4")
    expected = (result["low_estimate"] + result["high_estimate"]) / 2
    assert result["midpoint_estimate"] == expected

def test_total_rehab_includes_contingency():
    rooms = [
        {"room_type": "kitchen", "condition_grade": "C4", "renovation_needed": True,
         "issues_detected": ["outdated cabinets"], "priority": "high"},
        {"room_type": "bathroom", "condition_grade": "C4", "renovation_needed": True,
         "issues_detected": ["old fixtures"], "priority": "medium"}
    ]
    result = estimate_total_rehab_cost(rooms)
    assert result["contingency_percentage"] == 15
    assert result["total_low"] > result["subtotal_low"]
    assert result["recommended_budget"] > 0

def test_no_renovation_needed_skipped():
    rooms = [
        {"room_type": "kitchen", "condition_grade": "C1", "renovation_needed": False,
         "issues_detected": [], "priority": "none"}
    ]
    result = estimate_total_rehab_cost(rooms)
    assert result["recommended_budget"] == 0
    assert len(result["line_items"]) == 0