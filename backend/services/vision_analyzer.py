import os
import json
import base64
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

ANALYSIS_PROMPT = """
You are an expert real estate inspector and renovation estimator analyzing listing photos of a property.

Analyze the provided image and return a JSON object with exactly this structure:

{
  "room_type": "kitchen|bathroom|bedroom|dining_room|living_room|basement|exterior|roof|other",
  "condition_grade": "C1|C2|C3|C4|C5|C6",
  "condition_description": "Brief description of current condition",
  "issues_detected": ["list", "of", "specific", "issues", "you", "see"],
  "materials_identified": ["list", "of", "materials", "and", "finishes", "visible"],
  "renovation_needed": true or false,
  "priority": "none|low|medium|high|critical",
  "estimated_scope": "cosmetic|partial|full_renovation|structural"
}

Condition grades:
C1 = New/fully renovated, C2 = Near new, C3 = Well maintained,
C4 = Needs updating, C5 = Poor condition, C6 = Severely deteriorated

Be specific about what you actually see. Only return the JSON object, nothing else.
"""

def analyze_image_from_base64(image_base64: str, image_type: str = "image/jpeg") -> dict:
    try:
        image_bytes = base64.b64decode(image_base64)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_bytes(
                            data=image_bytes,
                            mime_type=image_type
                        ),
                        types.Part.from_text(text=ANALYSIS_PROMPT)
                    ]
                )
            ]
        )

        raw = response.text.strip()
        clean = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)
        result["analysis_successful"] = True
        return result

    except json.JSONDecodeError:
        return {
            "analysis_successful": False,
            "error": "Could not parse AI response as JSON",
            "raw_response": raw
        }
    except Exception as e:
      import traceback
      return {
          "analysis_successful": False,
          "error": str(e),
          "traceback": traceback.format_exc()
    }

def analyze_multiple_images(images: list[dict]) -> dict:
    results = []
    overall_grades = []

    for img in images:
        result = analyze_image_from_base64(
            img["base64"],
            img.get("type", "image/jpeg")
        )
        if result.get("analysis_successful"):
            results.append(result)
            overall_grades.append(result.get("condition_grade", "C3"))

    if not results:
        return {"error": "No images could be analyzed successfully"}

    grade_order = ["C1", "C2", "C3", "C4", "C5", "C6"]
    worst_grade = max(overall_grades, key=lambda g: grade_order.index(g))
    average_index = round(sum(grade_order.index(g) for g in overall_grades) / len(overall_grades))
    average_grade = grade_order[average_index]

    return {
        "total_images_analyzed": len(results),
        "overall_condition_grade": average_grade,
        "worst_condition_grade": worst_grade,
        "room_analyses": results,
        "analysis_successful": True
    }