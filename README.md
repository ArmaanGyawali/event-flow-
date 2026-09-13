# Event Booking Portal

A Streamlit web app for booking and managing events, built for university coursework using Python and object-oriented design.

## Features

- **User Roles**: Supports both Attendees and Event Organisers.
- **Event Discovery**: Search and filter events by category, venue, or title.
- **Multi-Tier Ticketing**: Buy tickets across different pricing tiers (General Admission, VIP) in a single checkout.
- **Organiser Tools**: Create new events, manage ticket capacities, and view booking stats.
- **Service Fees**: Automatically calculates a flat €2.00 fee per ticket.

---

## Project Structure

```text
working app demo/
│
├── app.py
├── database.py
├── run_app.py
├── requirements.txt
└── views/
    ├── auth.py
    ├── explore.py
    ├── bookings.py
    └── organiser.py

ow to Run the App
Option 1: Run as a Standalone Desktop App (Pre-built Release)
If you downloaded a pre-packaged release ZIP of the application:

Navigate to the dist/ folder in your downloaded directory.

Double-click the compiled application executable file to launch the app directly like a normal desktop program without needing terminal commands.

Option 2: Run from Source via Terminal
If you cloned the repository directly from GitHub:

Open your terminal and navigate into the project folder:

Bash
cd "working app demo"
Install dependencies:

Bash
pip install -r requirements.txt
Run the application via the launcher script:

Bash
streamlit run run_app.py
Open the local URL (http://localhost:8501) displayed in your terminal.
