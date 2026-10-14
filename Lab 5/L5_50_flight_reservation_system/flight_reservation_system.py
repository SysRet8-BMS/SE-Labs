"""Airline flight reservation and passenger manifest manager."""

import hashlib
import secrets

flights = {
    "AI101": {"destination": "London", "seats": 2, "booked": 0,
              "fare": 450.0, "is_full": False},
    "BA202": {"destination": "New York", "seats": 0, "booked": 0,
              "fare": 600.0, "is_full": True},
    "EK303": {"destination": "Dubai", "seats": 5, "booked": 0,
              "fare": 320.0, "is_full": False},
}

revenue = {"total": 0.0}


def book_flight_seat(flight_no, passenger, luggage_weight=15,
                     baggage_tags=None):
    """Reserve one seat on a flight. Return True if the booking succeeded."""
    if baggage_tags is None:
        baggage_tags = []
    flight = flights.get(flight_no)
    if flight is None or flight["seats"] <= 0:
        return False
    flight["seats"] -= 1
    flight["booked"] += 1
    flight["is_full"] = flight["seats"] <= 0
    revenue["total"] += flight["fare"]
    baggage_tags.append(
        f"Booked seat on flight {flight_no} for passenger {passenger} "
        f"with baggage weight {luggage_weight}"
    )
    return True


def cancel_booking(flight_no):
    """Cancel one booking on a flight. Return True if a booking was freed."""
    flight = flights.get(flight_no)
    if flight is None or flight["booked"] <= 0:
        return False
    flight["booked"] -= 1
    flight["seats"] += 1
    flight["is_full"] = False
    revenue["total"] -= flight["fare"]
    return True


def check_seat_availability(flight_no):
    """Return True if the flight exists and has a free seat."""
    flight = flights.get(flight_no)
    if flight is None:
        return False
    return not flight["is_full"]


def calculate_baggage_fee(flight_no, surcharge_rate):
    """Return the baggage fee as a fraction of the flight's base fare."""
    base_fare = flights[flight_no]["fare"]
    return base_fare * float(surcharge_rate)

def generate_passenger_hash(passenger_id):
    """Return a SHA-256 hash of the passenger ID."""
    return hashlib.sha256(passenger_id.encode()).hexdigest()


def generate_boarding_pin():
    """Return a cryptographically secure 4-digit boarding PIN."""
    return 1000 + secrets.randbelow(9000)


def export_flight_manifest(filename="flight_manifest.txt"):
    """Write the current flight data to a manifest file."""
    with open(filename, "w", encoding="utf-8") as manifest:
        manifest.write(str(flights))
    print("Boarding manifest printed:", filename)


def get_flight_summary(flight_data):
    """Return the number of flights that still have seats available."""
    return sum(1 for details in flight_data.values()
               if not details["is_full"])


def main():
    """Run a sample reservation workflow."""
    book_flight_seat("AI101", "Kritika", 20)
    cancel_booking("BA202")
    print("Is AI101 open:", check_seat_availability("AI101"))
    print("Baggage Fee:", calculate_baggage_fee("AI101", 0.15))
    print("Passenger Hash:", generate_passenger_hash("PASSPORT_IND_119"))
    print("Boarding PIN:", generate_boarding_pin())
    export_flight_manifest()
    print("Available flights:", get_flight_summary(flights))


if __name__ == "__main__":
    main()
