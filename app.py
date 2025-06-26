import os
import json
import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv
from langgraph_agent import run_agent

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Streamlit Page Setup
st.set_page_config(page_title="Appointment Bot", page_icon="🤖")
st.title("📅 Calendar Booking Assistant")

# 📌 Manual Booking Form
with st.form("booking_form"):
    st.subheader("🔹 Book a Meeting")

    date = st.date_input("Choose Date")
    start_time = st.time_input("Start Time")
    end_time = st.time_input("End Time")
    summary = st.text_input("Meeting Summary", value="Discussion")

    submitted = st.form_submit_button("📌 Book Appointment")

    if submitted:
        payload = {
            "intent": "book_meeting",
            "date": str(date),
            "start_time": start_time.strftime("%H:%M"),
            "end_time": end_time.strftime("%H:%M"),
            "summary": summary
        }

        try:
            response = requests.post("http://localhost:8000/book", json=payload)
            st.success("✅ Appointment Booked!")
            st.write("Status Code:", response.status_code)
            st.subheader("📨 Response from API:")
            st.json(response.json())

        except requests.exceptions.ConnectionError:
            st.error("❌ Backend not running. Please start FastAPI.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# 🧠 Assistant Interaction Section
st.subheader("💬 Talk to your Assistant")
user_msg = st.text_input("Say something like: 'Book a call with doctor tomorrow at 4PM'")

if user_msg:
    try:
        parsed_text = run_agent(user_msg)
        st.write("📋 Parsed Info:", parsed_text)

        # Try parsing as JSON
        try:
            parsed_json = json.loads(parsed_text)
            res = requests.post("http://localhost:8000/book", json=parsed_json)
            st.subheader("📨 Response from API:")
            st.json(res.json())
        except json.JSONDecodeError:
            st.warning("⚠️ Assistant response is not valid JSON. Please try a clearer request.")

    except Exception as e:
        st.error(f"❌ Error parsing or booking: {e}")
