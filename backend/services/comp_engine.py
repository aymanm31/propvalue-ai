from services.market_data import get_market_data_by_zip

def get_comp_analysis(zip_code: str, square_footage: float) -> dict:
    primary = get_market_data_by_zip(zip_code)

    if "error" in primary:
        return {"error": primary["error"]}

    neighboring_zips = primary.get("neighboring_zips", [])
    comp_data = []

    for nzip in neighboring_zips:
        neighbor = get_market_data_by_zip(nzip)
        if "error" not in neighbor:
            comp_data.append(neighbor)

    all_prices_per_sqft = [primary["median_price_per_sqft"]]
    all_sale_prices = [primary["median_sale_price"]]

    for comp in comp_data:
        all_prices_per_sqft.append(comp["median_price_per_sqft"])
        all_sale_prices.append(comp["median_sale_price"])

    avg_price_per_sqft = sum(all_prices_per_sqft) / len(all_prices_per_sqft)
    min_price_per_sqft = min(all_prices_per_sqft)
    max_price_per_sqft = max(all_prices_per_sqft)

    arv_estimate = avg_price_per_sqft * square_footage
    arv_low = min_price_per_sqft * square_footage
    arv_high = max_price_per_sqft * square_footage

    return {
        "zip_code": zip_code,
        "square_footage": square_footage,
        "primary_market": {
            "median_price_per_sqft": primary["median_price_per_sqft"],
            "median_sale_price": primary["median_sale_price"],
            "days_on_market": primary["days_on_market"]
        },
        "comps_used": len(comp_data) + 1,
        "neighboring_zips_found": len(comp_data),
        "avg_price_per_sqft": round(avg_price_per_sqft, 2),
        "min_price_per_sqft": round(min_price_per_sqft, 2),
        "max_price_per_sqft": round(max_price_per_sqft, 2),
        "arv_estimate": round(arv_estimate, 2),
        "arv_low": round(arv_low, 2),
        "arv_high": round(arv_high, 2),
        "arv_confidence": "high" if len(comp_data) >= 2 else "medium" if len(comp_data) == 1 else "low"
    }