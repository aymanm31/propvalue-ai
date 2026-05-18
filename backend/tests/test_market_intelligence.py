from services.market_intelligence import check_over_improvement

def test_no_alert_for_safe_deal():
    result = check_over_improvement(
        zip_code="22030",
        projected_arv=500000,
        rehab_cost=40000,
        purchase_price=320000
    )
    assert "error" not in result
    assert result["is_over_improved"] == False

def test_alert_triggered_for_over_improvement():
    result = check_over_improvement(
        zip_code="22030",
        projected_arv=800000,
        rehab_cost=200000,
        purchase_price=400000
    )
    assert "error" not in result
    assert result["alert_count"] > 0

def test_neighborhood_ceiling_calculated():
    result = check_over_improvement(
        zip_code="22030",
        projected_arv=500000,
        rehab_cost=40000,
        purchase_price=320000
    )
    assert result["neighborhood_ceiling"] == round(548000 * 1.25, 2)

def test_invalid_zip_returns_error():
    result = check_over_improvement(
        zip_code="00000",
        projected_arv=500000,
        rehab_cost=40000,
        purchase_price=320000
    )
    assert "error" in result