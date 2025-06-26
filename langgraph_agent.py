import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Raise error if key not found
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found. Make sure it is set in the .env file.")

# Create LLM instance
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key)


def extract_booking_info(message: str):
    prompt = f"""
You are a helpful assistant that extracts scheduling information from user input.

Extract the following fields from this message:
- intent (always "book_meeting")
- date (in YYYY-MM-DD format)
- start_time (in HH:MM, 24-hour format)
- end_time (in HH:MM, 24-hour format)
- summary (short title for the meeting)

User message:
\"\"\"{message}\"\"\"

Respond ONLY in this JSON format (no explanation):
{{
  "intent": "book_meeting",
  "date": "YYYY-MM-DD",
  "start_time": "HH:MM",
  "end_time": "HH:MM",
  "summary": "short summary"
}}
"""
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        return f"❌ Error extracting booking info: {e}"


def run_agent(user_input: str) -> str:
    print(f"🧠 Processing input: {user_input}")

    if "cancel" in user_input.lower():
        return "Canceling your appointment..."
    elif "book" in user_input.lower() or "schedule" in user_input.lower():
        return extract_booking_info(user_input)
    else:
        return "Sorry, I didn't understand that."
