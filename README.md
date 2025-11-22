Inkle Tourism – Multi-Agent AI System
AI Intern Assignment – Completed by Sree Vaishnavi V (1CR22AI110)
This project implements a multi-agent tourism assistant that helps users get:

✔ Real-time weather

✔ Nearby tourist attractions

✔ Error handling for unknown places

✔ Full end-to-end deployment (backend + frontend)

The backend uses FastAPI, and the system is built around three specialized agents:

GeocodingAgent → Validates location (Nominatim API)

WeatherAgent → Gets weather (Open-Meteo API)

PlacesAgent → Fetches attractions (Overpass API)

The parent agent (TourismOrchestrator) extracts intent, coordinates all agents, and formats the final response.

🚀 Live Demo
Frontend (main application link):
🔗 https://deft-conkies-526391.netlify.app

Backend API (Render):
🔗 https://inkle-tourism-backend-0i9q.onrender.com

API Docs (Swagger):
🔗 https://inkle-tourism-backend-0i9q.onrender.com/docs

📁 Repository Structure
bash
Copy code
inkle_tourism/
│
├── backend/
│   ├── main.py                    # FastAPI main entrypoint
│   ├── agents/
│   │   ├── geocoding_agent.py     # Nominatim API
│   │   ├── weather_agent.py       # Open-Meteo API
│   │   └── places_agent.py        # Overpass API
│   └── orchestrator/
│       └── tourism_orchestrator.py
│
├── frontend/
│   └── index.html                 # Minimal UI for user queries
│
└── requirements.txt
🧠 How It Works
User enters:
“I'm going to go to Bangalore, what's the temperature there?”

The Orchestrator:

Extracts the place (“Bangalore”)

Validates using GeocodingAgent

Detects intent (weather + places)

Calls:

WeatherAgent → temp + rain %

PlacesAgent → top 5 attractions

Returns a combined, formatted response.

If the place does not exist →
❌ "I don't know this place exists."

🔌 APIs Used
Feature	Agent	API
Location → coordinates	GeocodingAgent	Nominatim (OpenStreetMap)
Weather	WeatherAgent	Open-Meteo
Attractions	PlacesAgent	Overpass (OpenStreetMap)

🛠 Tech Stack
Python 3

FastAPI

httpx

Render (backend)

Netlify (frontend)

HTML + JS (simple UI)

🧪 Example Queries
Try these in the live demo:

“I'm going to go to Bangalore, let's plan my trip.”

“I'm going to go to Chennai, what is the temperature there?”

“I'm going to Delhi, what places can I visit?”

✨ Features
Multi-agent architecture

Real API calls (not hardcoded)

Automatic intent detection

Error handling

Fully deployed frontend + backend

Clean modular structure

🧩 Challenges Faced
Extracting place names from flexible queries

Overpass API returning noisy/missing results

Handling multi-API timeouts & errors

CORS configuration between Render & Netlify

Ensuring clean responses matching assignment examples

👩‍💻 Developer
Sree Vaishnavi V
