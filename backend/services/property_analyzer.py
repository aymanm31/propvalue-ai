from services.vision_analyzer import analyze_multiple_images
from services.cost_estimator import estimate_total_rehab_cost
from services.market_data import estimate_arv
from services.roi_engine import ROIInput, calculate_roi
from services.market_intelligence import check_over_improvement
from services.comp_engine import get_comp_analysis

def run_full_analysis(
    images: list[dict],
    zip_code: str,
    square_footage: float,
    purchase_price: float,
    monthly_taxes: float,
    monthly_insurance: float,
    rehab_duration_months: int
) -> dict:

    vision_result = analyze_multiple_images(images)
    if not vision_result.get("analysis_successful"):
        return {"error": "Photo analysis failed", "details": vision_result}

    room_analyses = vision_result.get("room_analyses", [])
    cost_result = estimate_total_rehab_cost(room_analyses, zip_code=zip_code)
    rehab_cost = cost_result["recommended_budget"]

    comp_result = get_comp_analysis(zip_code, square_footage)
    if "error" in comp_result:
        return {"error": "ARV estimation failed", "details": comp_result}

    arv = comp_result["arv_estimate"]
    arv_result = comp_result

    over_improvement = check_over_improvement(
        zip_code=zip_code,
        projected_arv=arv,
        rehab_cost=rehab_cost,
        purchase_price=purchase_price
    )

    roi_input = ROIInput(
        purchase_price=purchase_price,
        rehab_cost=rehab_cost,
        arv=arv,
        monthly_taxes=monthly_taxes,
        monthly_insurance=monthly_insurance,
        rehab_duration_months=rehab_duration_months
    )
    roi_result = calculate_roi(roi_input)

    return {
        "property": {
            "zip_code": zip_code,
            "square_footage": square_footage,
            "purchase_price": purchase_price
        },
        "vision_analysis": {
            "overall_condition_grade": vision_result["overall_condition_grade"],
            "worst_condition_grade": vision_result["worst_condition_grade"],
            "images_analyzed": vision_result["total_images_analyzed"],
            "room_analyses": room_analyses
        },
        "rehab_estimate": cost_result,
        "market_data": arv_result,
        "roi_analysis": roi_result.breakdown,
        "over_improvement": over_improvement
    }