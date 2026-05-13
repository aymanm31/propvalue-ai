import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/zip_market_data.json")

def get_market_data_by_zip(zip_code: str) -> dict:
    if not os.path.exists(DATA_PATH):
        return {"error": "Market data file not found"}

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if zip_code not in data:
        return {"error": f"No data found for ZIP code {zip_code}. Available ZIPs: {list(data.keys())}"}

    return data[zip_code]

def estimate_arv(zip_code: str, square_footage: float) -> dict:
    market = get_market_data_by_zip(zip_code)

    if "error" in market:
        return market

    arv = market["median_price_per_sqft"] * square_footage

    return {
        "zip_code": zip_code,
        "square_footage": square_footage,
        "median_price_per_sqft": market["median_price_per_sqft"],
        "estimated_arv": round(arv, 2),
        "market_median_sale_price": market["median_sale_price"],
        "days_on_market": market["days_on_market"],
        "period": market["period"]
    }