# Clinic Assistant (AI Symptom Checker + Appointment Booking)

A healthcare web app built with Flask, SQLite and the Google Gemini API.

## Features
- Symptom checker: the patient describes symptoms and the AI suggests which type of specialist to see, with urgency, reason and warning signs
- Emergency handling: for emergency symptoms the app shows a red warning (call 112) and hides the booking button
- Appointment booking: name, phone and date are saved in a SQLite database
- Appointments list page

This tool gives general guidance only and is not a medical diagnosis.

## Tech
Python, Flask, SQLite, HTML/CSS (Jinja templates), Google Gemini API (google-genai)

## Run locally
1. Install Python 3.9 or newer
2. python -m venv venv
3. venv\Scripts\activate
4. pip install -r requirements.txt
5. Copy .env.example to .env and put your Gemini API key in it (free key from aistudio.google.com)
6. python app.py
7. Open http://127.0.0.1:5000

## Pages
- / : home
- /triage : AI symptom checker
- /book : book an appointment
- /appointments : list of appointments

## Prompt engineering
The AI prompt was improved from a simple first version to a structured version (role, rules, JSON output, India context). See the prompt documentation submitted with this project.