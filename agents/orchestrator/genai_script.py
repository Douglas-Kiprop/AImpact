import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_GENERATIVEAI_API_KEY")
print(f"API Key: {api_key}")
genai.configure(api_key=api_key)
try:
    model = genai.GenerativeModel('gemini-1.5-flash-001')
    response = model.generate_content("Say hello")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
