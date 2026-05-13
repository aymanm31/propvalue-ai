import pytest
from services.market_data import get_market_data_by_zip, estimate_arv

def test_valid_zip_returns_data():
    result = get_market_data_by_zip("22030")
    assert "error" not in result
    assert result["city"] == "Fairfax"
    assert result["median_sale_price"] > 0

def test_invalid_zip_returns_error():
    result = get_market_data_by_zip("00000")
    assert "error" in result

def test_arv_estimate_calculation():
    result = estimate_arv("22030", 1500)
    assert "error" not in result
    assert result["estimated_arv"] == 323 * 1500
    assert result["square_footage"] == 1500

def test_arv_estimate_invalid_zip():
    result = estimate_arv("00000", 1500)
    assert "error" in result