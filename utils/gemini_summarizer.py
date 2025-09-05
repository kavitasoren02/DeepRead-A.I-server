import google.generativeai as genai
import re

genai.configure(api_key = "AIzaSyBNw1in9bktKqhIx_v1K4sXkbD_hWahqQU")

model = genai.GenerativeModel(model_name="gemini-2.5-pro")

def get_summary_from_text(text: str) -> str:
    # prompt = f"Summarize the following content clearly and concisely: \n\n{text}"
    try:
        clean_text = re.sub(r"\s+", " ", re.sub(r"[\*\n\\]", " ", text)).strip()
        response = model.generate_content(clean_text)
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"
