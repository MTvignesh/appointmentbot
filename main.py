from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google_calendar import check_availability, book_event

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BookingRequest(BaseModel):
    intent: str
    date: str
    start_time: str
    end_time: str
    summary: str

@app.post("/book")
def book_meeting(data: BookingRequest):
    try:
        if data.intent != "book_meeting":
            return {"status": "ignored", "message": "Unknown intent"}

        if not check_availability(data.date, data.start_time, data.end_time):
            return {"status": "unavailable", "message": "Time slot is already booked"}

        event = book_event(data.date, data.start_time, data.end_time, data.summary)
        return {"status": "success", "message": "Booking confirmed", "event": event}

    except Exception as e:
        return {"status": "error", "message": str(e)}
