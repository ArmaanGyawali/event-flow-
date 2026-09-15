# 🎫 Event Booking Portal

Hey! Welcome to my Event Booking Portal. I built this project as a modular, multi-role web application using **Streamlit** and Python. It handles everything from event creation and multi-tier ticket management to attendee bookings and seamless role-based navigation.

## ✨ What I Built Into This App

- **Multi-Role Authentication**: Secure login supporting distinct workflows depending on whether you log in as an **Organiser** or an **Attendee**.
- **Organiser Dashboard & Controls**:
  - Publish new events with custom image support (paste a URL or upload an image file directly).
  - Configure flexible ticket tiers with custom pricing and quantities.
  - Update event statuses (Active / Cancelled) or archive deleted events safely.
  - Inspect real-time attendee bookings tied to specific events.
- **Attendee Experience**:
  - Explore active events with category filtering and clear details.
  - Book tickets smoothly without running into annoying UI reset bugs.
- **Smart State Management**: I structured the session state carefully to eliminate page-jump glitches and widget state mismatches during state transitions.

## 🛠️ Tech Stack I Used

- **Frontend & UI**: Streamlit
- **Core Logic**: Python
- **Data Layer**: In-memory architecture using custom Python classes (`database.py`)

## 🚀 How to Run My Project Locally

If you want to spin up and test my code on your machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ArmaanGyawali/event-flow-.git](https://github.com/ArmaanGyawali/event-flow-.git)
   cd event-flow

1. Install Streamlit:
   pip install streamlit

2. Run the app:
   streamlit run app.py

📂 Project Structure
Here is how I organized my codebase:

event-flow/
│
├── app.py              # Main entry point, routing, and session navigation state
├── database.py         # Data models (Events, Bookings, Ticket Types)
└── views/              # Modular view components
    ├── auth.py         # Login & Registration views
    ├── explore.py      # Attendee event exploration
    ├── bookings.py     # Attendee booking management
    └── organiser.py    # Organiser dashboard & event controls

