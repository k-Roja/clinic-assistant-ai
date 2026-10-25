import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODELS = ["gemini-3.5-flash", "gemini-2.5-flash"]
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# V1 (first version, kept for prompt documentation):
# "Which type of doctor should I see for these symptoms: {symptoms}"

PROMPT_V2 = """You are a symptom-to-specialist guide for a clinic in India.
A patient describes their symptoms. Suggest which type of doctor they should see.

Rules:
- Do NOT diagnose any disease and do NOT recommend medicines.
- Suggest exactly one main specialist type (for example: General Physician, Dermatologist, ENT Specialist, Cardiologist).
- Choose urgency: "Routine" (book within a week), "Soon" (book within 1-2 days) or "Emergency" (go to hospital now).
- If symptoms may be life-threatening (chest pain, trouble breathing, stroke signs, heavy bleeding, unconsciousness), urgency must be "Emergency".
- Use plain, simple English. No markdown, no emojis, no US-specific references. For emergencies mention calling 112 (India).
- Keep the reason to 2 sentences at most.

Return ONLY valid JSON with exactly these keys:
{{"specialist": "...", "urgency": "...", "reason": "...", "warning_signs": ["...", "..."]}}

Patient symptoms: {symptoms}
"""


def get_triage(symptoms):
    for model in MODELS:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=PROMPT_V2.format(symptoms=symptoms),
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                )
                data = json.loads(response.text)
                data["disclaimer"] = "This is not a medical diagnosis. Please consult a qualified doctor."
                return data
            except Exception as e:
                error = str(e)
                if "API_KEY_INVALID" in error:
                    return {"error": "API key problem. Please check the .env file."}
                if "429" in error:
                    return {"error": "Too many requests. Please wait 1 minute and try again."}
                if "503" in error:
                    time.sleep(2)
                    continue
                break
    return {"error": "The AI service is busy right now. Please try again in a minute."}