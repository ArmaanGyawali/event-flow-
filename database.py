# database.py - Full mock store with 10 default events and pre-seeded ticket tiers
class Event:
    def __init__(
        self,
        event_id,
        title,
        description,
        category,
        date,
        time,
        location,
        image_url,
        organiser_id,
        status="Active",
        artist="N/A",
    ):
        self.event_id = event_id
        self.title = title
        self.description = description
        self.category = category
        self.date = date
        self.time = time
        self.location = location
        self.image_url = image_url
        self.organiser_id = organiser_id
        self.status = status
        self.artist = artist
        self.ticket_types = []
        self.is_deleted = False

    def add_ticket_type(self, ticket_type):
        self.ticket_types.append(ticket_type)


class TicketType:
    def __init__(self, ticket_type_id, name, price, quantity):
        self.ticket_type_id = ticket_type_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.available_quantity = quantity


class Booking:
    def __init__(
        self,
        booking_id,
        attendee_id,
        event_id,
        event_title,
        ticket_type_id,
        ticket_type_name,
        count,
        total_price,
        booking_date,
        status="Confirmed",
    ):
        self.booking_id = booking_id
        self.attendee_id = attendee_id
        self.event_id = event_id
        self.event_title = event_title
        self.ticket_type_id = ticket_type_id
        self.ticket_type_name = ticket_type_name
        self.count = count
        self.total_price = total_price
        self.booking_date = booking_date
        self.status = status


class User:
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password


class Attendee(User):
    pass


class EventOrganiser(User):
    pass


users = {
    "att1": Attendee("att1", "John Doe", "john@test.com", "password123"),
    "org1": EventOrganiser("org1", "Sarah Connor", "org@test.com", "password123"),
}

events = [
    Event("evt_1", "PyCon Europe 2026", "Premier European Python developer conference.", "Tech", "2026-09-15", "09:00 AM", "Estrel Congress Center, Berlin", "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800", "org1", "Active", "Guido van Rossum"),
    Event("evt_2", "Coldplay: Music of the Spheres", "Immersive stadium concert experience.", "Music", "2026-10-02", "07:30 PM", "Olympiastadion, Berlin", "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=800", "org1", "Active", "Coldplay"),
    Event("evt_3", "Tech Summit Berlin", "Exploring AI, cloud architecture, and modern paradigms.", "Tech", "2026-11-20", "10:00 AM", "Berlin Congress Center", "https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=800", "org1", "Active", "Various Speakers"),
    Event("evt_4", "Berlin Marathon Expo", "Annual international marathon runner gathering.", "Sports", "2026-09-25", "08:00 AM", "Tempelhof Airport, Berlin", "https://images.unsplash.com/photo-1452626038306-9aae5e071dd3?w=800", "org1", "Active", "N/A"),
    Event("evt_5", "Startup Pitch Night", "Venture capital networking and pitch showcase.", "Conference", "2026-10-12", "06:00 PM", "Factorial workspace, Berlin", "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=800", "org1", "Active", "Berlin Founders"),
    Event("evt_6", "Electronic Beats Festival", "Underground techno and electronic music showcase.", "Music", "2026-10-30", "10:00 PM", "Kraftwerk Berlin", "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800", "org1", "Active", "DJ Koze"),
    Event("evt_7", "Cybersecurity Hackathon 2026", "48-hour ethical hacking and defense challenge.", "Tech", "2026-11-05", "09:00 AM", "Hasso Plattner Institute", "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800", "org1", "Active", "SecOps Team"),
    Event("evt_8", "Global AI Ethics Forum", "Discussing responsible AI development and regulation.", "Conference", "2026-11-15", "01:00 PM", "Urania Berlin", "https://images.unsplash.com/photo-1591115765373-5207764f72e4?w=800", "org1", "Active", "Dr. Elena Rostova"),
    Event("evt_9", "Indie Rock Night", "Live performances featuring top indie rock bands.", "Music", "2026-12-01", "08:00 PM", "Astra Kulturhaus, Berlin", "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800", "org1", "Active", "The Arctic Echoes"),
    Event("evt_10", "E-Sports Championship Final", "Top international teams compete for the trophy.", "Sports", "2026-12-10", "02:00 PM", "Verti Music Hall, Berlin", "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=800", "org1", "Active", "Fnatic vs G2"),
]

# Automatically seed default ticket tiers for all 10 events
for ev in events:
    ev.add_ticket_type(TicketType(f"tix_{ev.event_id}_1", "General Admission", 45.0, 100))
    ev.add_ticket_type(TicketType(f"tix_{ev.event_id}_2", "VIP Pass", 95.0, 25))

bookings = []