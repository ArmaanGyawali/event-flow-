import os

readme_content = """# 🎟️ Event Booking Portal

A modular, production-ready **Event Booking Portal** built with **Streamlit**, adhering to UML-based architectural requirements and object-oriented design principles. The platform supports multi-tier ticketing, integrated service fees, real-time inventory management, and role-based access control (RBAC) for Attendees and Event Organisers.

---

## 🌟 Key Features

### 👤 For Attendees
- **Explore & Filter Events**: Browse active events by category (Tech, Music, Sports, Conference, etc.) or search dynamically by title, artist, or venue.
- **Multi-Tier Ticket Checkout**: Purchase multiple ticket quantities across different tiers (e.g., General Admission and VIP Passes) simultaneously in a single checkout flow.
- **Transparent Pricing**: Automatically calculates flat platform service fees (€2.00) per ticket alongside base tier pricing.
- **Booking Management**: Track booking history, statuses, and confirmed reservations instantly.

### 📊 For Event Organisers
- **Event Lifecycle Management**: Create, update, or remove events with custom metadata, venues, dates, and banner images.
- **Ticket Tier Configuration**: Define and manage multi-tier pricing and seat capacities per event.
- **Dashboard & Analytics**: Monitor total bookings, revenue metrics, and attendee engagement.

---

## 🏗️ System Architecture & Structure

The codebase is organized into a clean, modular structure separating business logic, data models, and UI views:

```text
working app demo/
│
├── app.py                  # Main Streamlit router & session-state controller
├── database.py             # Object-Oriented models (User, Attendee, EventOrganiser, Event, TicketType, Booking)
└── views/
    ├── auth.py             # User login and registration interface
    ├── explore.py          # Event catalog, search/filter, and multi-tier checkout
    ├── bookings.py         # Attendee booking history and ticket details
    └── organiser.py        # Organiser dashboard, event creation, and tier management