import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/labor_multipliers.json")

def get_labor_multiplier(zip_code: str, state: str = "") -> dict:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if zip_code in data["zip_overrides"]:
        multiplier = data["zip_overrides"][zip_code]
        source = "zip_code"
    elif state.upper() in data["state_multipliers"]:
        multiplier = data["state_multipliers"][state.upper()]
        source = "state"
    else:
        multiplier = data["default"]
        source = "national_average"

    return {
        "zip_code": zip_code,
        "multiplier": multiplier,
        "source": source,
        "description": f"Labor costs in this area are "
                       f"{'above' if multiplier > 1 else 'below'} "
                       f"the national average by "
                       f"{abs(round((multiplier - 1) * 100, 0)):.0f}%"
                       if multiplier != 1.0 else
                       "Labor costs in this area match the national average"
    }