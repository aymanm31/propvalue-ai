import base64
import os
from dotenv import load_dotenv

load_dotenv()

print("API Key found:", bool(os.getenv("GEMINI_API_KEY")))
print("API Key starts with:", os.getenv("GEMINI_API_KEY")[:10])

with open("C:/Users/qadee/Downloads/Screenshot 2026-05-13 214209.jpeg", "rb") as f:
    image_bytes = f.read()
    image_base64 = base64.b64encode(image_bytes).decode()

print("Image loaded, size:", len(image_bytes), "bytes")
print("Base64 length:", len(image_base64))

from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# for model in client.models.list():
#     print(model.name)

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/jpeg"
                    ),
                    types.Part.from_text(text="What do you see in this image? One sentence only.")
                ]
            )
        ]
    )
    print("SUCCESS:", response.text)
except Exception as e:
    import traceback
    print("FULL ERROR:")
    traceback.print_exc()