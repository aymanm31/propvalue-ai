from dataclasses import dataclass

@dataclass
class ROIInput:
    purchase_price: float
    rehab_cost: float
    arv: float
    monthly_taxes: float
    monthly_insurance: float
    rehab_duration_months: int

@dataclass
class ROIResult:
    purchase_price: float
    rehab_cost: float
    arv: float
    holding_cost: float
    total_investment: float
    net_profit: float
    roi_percentage: float
    seventy_percent_max: float
    is_good_deal: bool
    verdict: str
    breakdown: dict

def calculate_holding_cost(
    monthly_taxes: float,
    monthly_insurance: float,
    rehab_duration_months: int
) -> float:
    monthly_total = monthly_taxes + monthly_insurance
    return monthly_total * rehab_duration_months

def calculate_roi(input: ROIInput) -> ROIResult:
    holding_cost = calculate_holding_cost(
        input.monthly_taxes,
        input.monthly_insurance,
        input.rehab_duration_months
    )

    total_investment = input.purchase_price + input.rehab_cost + holding_cost
    net_profit = input.arv - total_investment
    roi_percentage = (net_profit / total_investment) * 100

    seventy_percent_max = (input.arv * 0.70) - input.rehab_cost

    is_good_deal = (
        input.purchase_price <= seventy_percent_max and
        roi_percentage >= 15
    )

    if roi_percentage >= 20 and is_good_deal:
        verdict = "Strong deal"
    elif roi_percentage >= 15 and is_good_deal:
        verdict = "Good deal"
    elif roi_percentage >= 10:
        verdict = "Marginal deal — proceed with caution"
    elif roi_percentage >= 0:
        verdict = "Weak deal — likely not worth it"
    else:
        verdict = "Bad deal — you would lose money"

    breakdown = {
        "purchase_price": round(input.purchase_price, 2),
        "rehab_cost": round(input.rehab_cost, 2),
        "holding_cost": round(holding_cost, 2),
        "total_investment": round(total_investment, 2),
        "arv": round(input.arv, 2),
        "net_profit": round(net_profit, 2),
        "roi_percentage": round(roi_percentage, 2),
        "seventy_percent_rule_max_purchase": round(seventy_percent_max, 2),
        "passes_70_percent_rule": input.purchase_price <= seventy_percent_max
    }

    return ROIResult(
        purchase_price=input.purchase_price,
        rehab_cost=input.rehab_cost,
        arv=input.arv,
        holding_cost=holding_cost,
        total_investment=total_investment,
        net_profit=net_profit,
        roi_percentage=roi_percentage,
        seventy_percent_max=seventy_percent_max,
        is_good_deal=is_good_deal,
        verdict=verdict,
        breakdown=breakdown
    )