import base64
import requests

with open("C:/Users/qadee/Downloads/Screenshot 2026-05-13 214209.jpeg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

response = requests.post(
    "http://localhost:8000/api/analyze/photos",
    json={
        "images": [
            {
                "base64": image_data,
                "type": "image/jpeg"
            }
        ]
    }
)

print(response.json())