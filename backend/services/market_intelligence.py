from services.market_data import get_market_data_by_zip

OVER_IMPROVEMENT_THRESHOLD = 0.90

def check_over_improvement(
    zip_code: str,
    projected_arv: float,
    rehab_cost: float,
    purchase_price: float
) -> dict:
    market = get_market_data_by_zip(zip_code)

    if "error" in market:
        return {"error": market["error"]}

    neighborhood_ceiling = market["median_sale_price"] * 1.25
    arv_to_ceiling_ratio = projected_arv / neighborhood_ceiling
    is_over_improved = arv_to_ceiling_ratio > OVER_IMPROVEMENT_THRESHOLD

    total_invested = purchase_price + rehab_cost
    recommended_max_rehab = neighborhood_ceiling * 0.70 - purchase_price

    alerts = []

    if is_over_improved:
        alerts.append(
            f"Your projected ARV of ${projected_arv:,.0f} is "
            f"{arv_to_ceiling_ratio * 100:.0f}% of the neighborhood ceiling "
            f"(${neighborhood_ceiling:,.0f}). Buyers in this area rarely pay "
            f"above the ceiling regardless of renovation quality."
        )

    if rehab_cost > recommended_max_rehab and recommended_max_rehab > 0:
        alerts.append(
            f"Your rehab budget of ${rehab_cost:,.0f} exceeds the recommended "
            f"maximum of ${recommended_max_rehab:,.0f} for this neighborhood. "
            f"Consider scaling back the renovation scope."
        )

    if total_invested > neighborhood_ceiling * 0.85:
        alerts.append(
            f"Your total investment of ${total_invested:,.0f} leaves very little "
            f"margin before hitting the neighborhood ceiling of "
            f"${neighborhood_ceiling:,.0f}."
        )

    return {
        "neighborhood_ceiling": round(neighborhood_ceiling, 2),
        "projected_arv": round(projected_arv, 2),
        "arv_to_ceiling_ratio": round(arv_to_ceiling_ratio * 100, 1),
        "is_over_improved": is_over_improved,
        "recommended_max_rehab": round(max(recommended_max_rehab, 0), 2),
        "alerts": alerts,
        "alert_count": len(alerts)
    }