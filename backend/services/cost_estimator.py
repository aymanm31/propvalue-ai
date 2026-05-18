import os
import json

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/labor_multipliers.json")

REHAB_COSTS = {
    "kitchen": {
        "C1": {"low": 0, "high": 0},
        "C2": {"low": 2000, "high": 5000},
        "C3": {"low": 8000, "high": 20000},
        "C4": {"low": 20000, "high": 40000},
        "C5": {"low": 40000, "high": 70000},
        "C6": {"low": 70000, "high": 120000}
    },
    "bathroom": {
        "C1": {"low": 0, "high": 0},
        "C2": {"low": 1000, "high": 3000},
        "C3": {"low": 5000, "high": 12000},
        "C4": {"low": 12000, "high": 25000},
        "C5": {"low": 25000, "high": 45000},
        "C6": {"low": 45000, "high": 75000}
    },
    "bedroom": {
        "C1": {"low": 0, "high": 0},
        "C2": {"low": 500, "high": 1500},
        "C3": {"low": 2000, "high": 6000},
        "C4": {"low": 6000, "high": 15000},
        "C5": {"low": 15000, "high": 30000},
        "C6": {"low": 30000, "high": 55000}
    },
    "living_room": {
        "C1": {"low": 0, "high": 0},
        "C2": {"low": 500, "high": 2000},
        "C3": {"low": 3000, "high": 8000},
        "C4": {"low": 8000, "high": 18000},
        "C5": {"low": 18000, "high": 35000},
        "C6": {"low": 35000, "high": 60000}
    },
    "basement": {
        "C1": {"low": 0, "high": 0},
        "C2": {"low": 1000, "high": 3000},
        "C3": {"low": 5000, "high": 15000},
        "C4": {"low": 15000, "high": 35000},
        "C5": {"low": 35000, "high": 65000},
        "C6": {"low": 65000, "high": 110000}
    },
    "exterior": {
        "C1": {"low": 0, "high": 0},
        "C2": {"low": 1000, "high": 4000},
        "C3": {"low": 5000, "high": 15000},
        "C4": {"low": 15000, "high": 35000},
        "C5": {"low": 35000, "high": 70000},
        "C6": {"low": 70000, "high": 130000}
    },
    "roof": {
        "C1": {"low": 0, "high": 0},
        "C2": {"low": 500, "high": 2000},
        "C3": {"low": 3000, "high": 8000},
        "C4": {"low": 8000, "high": 18000},
        "C5": {"low": 18000, "high": 35000},
        "C6": {"low": 35000, "high": 65000}
    },
    "other": {
        "C1": {"low": 0, "high": 0},
        "C2": {"low": 500, "high": 1500},
        "C3": {"low": 2000, "high": 5000},
        "C4": {"low": 5000, "high": 12000},
        "C5": {"low": 12000, "high": 25000},
        "C6": {"low": 25000, "high": 50000}
    }
}

def get_labor_multiplier_value(zip_code: str) -> float:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if zip_code in data["zip_overrides"]:
        return data["zip_overrides"][zip_code]
    return data["default"]

def estimate_room_cost(
    room_type: str,
    condition_grade: str,
    labor_multiplier: float = 1.0
) -> dict:
    room = REHAB_COSTS.get(room_type, REHAB_COSTS["other"])
    costs = room.get(condition_grade, {"low": 0, "high": 0})
    low = round(costs["low"] * labor_multiplier, 2)
    high = round(costs["high"] * labor_multiplier, 2)
    return {
        "room_type": room_type,
        "condition_grade": condition_grade,
        "labor_multiplier": labor_multiplier,
        "low_estimate": low,
        "high_estimate": high,
        "midpoint_estimate": round((low + high) / 2, 2)
    }

def estimate_total_rehab_cost(
    room_analyses: list[dict],
    zip_code: str = ""
) -> dict:
    labor_multiplier = get_labor_multiplier_value(zip_code) if zip_code else 1.0
    line_items = []
    total_low = 0
    total_high = 0

    for room in room_analyses:
        if not room.get("renovation_needed", False):
            continue

        room_type = room.get("room_type", "other")
        grade = room.get("condition_grade", "C3")
        estimate = estimate_room_cost(room_type, grade, labor_multiplier)

        line_items.append({
            "room_type": room_type,
            "condition_grade": grade,
            "issues": room.get("issues_detected", []),
            "priority": room.get("priority", "medium"),
            "low_estimate": estimate["low_estimate"],
            "high_estimate": estimate["high_estimate"],
            "midpoint_estimate": estimate["midpoint_estimate"]
        })

        total_low += estimate["low_estimate"]
        total_high += estimate["high_estimate"]

    contingency_pct = 0.15
    total_low_with_contingency = round(total_low * (1 + contingency_pct), 2)
    total_high_with_contingency = round(total_high * (1 + contingency_pct), 2)
    midpoint = round((total_low_with_contingency + total_high_with_contingency) / 2, 2)

    return {
        "line_items": line_items,
        "labor_multiplier": labor_multiplier,
        "subtotal_low": round(total_low, 2),
        "subtotal_high": round(total_high, 2),
        "contingency_percentage": contingency_pct * 100,
        "total_low": total_low_with_contingency,
        "total_high": total_high_with_contingency,
        "recommended_budget": midpoint
    }