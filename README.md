# EventFlow - Event Booking Portal

EventFlow is a full-featured Event Booking Portal built using **Streamlit**. It supports both traditional terminal-based development and standalone desktop application packaging for macOS.

---

## Features

* **Event Discovery & Booking**: Browse available events, view detailed schedules, and manage bookings seamlessly.
* **Dual Execution Modes**: Run the portal locally via the terminal for development, or launch it as a standalone double-clickable desktop app.
* **Persistent Database**: Integrated backend tracking for events and user data.

---

## Prerequisites

* **Python 3.10+** installed on your system.
* **Git** for version control.

---

## 1. Local Development (Terminal)

To run the application locally in your browser for development or testing:

* Clone the repository and navigate into the project directory:
  ```bash
  cd "working app demo"




Create and activate a virtual environment:

Bash
python3 -m venv .venv
source .venv/bin/activate
Install the required dependencies:

Bash
pip install -r requirements.txt
Launch the Streamlit development server:

Bash
streamlit run app.py
Open your browser and navigate to http://localhost:8501.

2. Standalone Desktop App (macOS)
To build and run EventFlow as a standalone, double-clickable application executable:

Ensure your virtual environment is active and dependencies are installed.

Build the executable using PyInstaller and the custom configuration spec:

Bash
pyinstaller run_app.spec
Open the newly generated dist/ folder inside your project directory.

Double-click the EventFlow application icon to launch it directly.

Repository Structure
app.py: Core Streamlit application logic and UI.

run_app.py: Application launcher script configured to bypass context errors during standalone packaging.

run_app.spec: PyInstaller build configuration file for bundling EventFlow.

database.py: Database connection and management modules.

requirements.txt: Project Python dependencies.
