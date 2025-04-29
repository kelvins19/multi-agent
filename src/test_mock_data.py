"""
Test script for the mock data.
This script demonstrates how to use the mock data directly.
"""

from src.data.mock_data import get_flights, get_hotels, get_destinations

def main():
    # Test flight data
    print("=== FLIGHT DATA ===")
    flights = get_flights("New York", "Paris", "2023-06-15")
    for i, flight in enumerate(flights, 1):
        print(f"\nFlight {i}:")
        print(f"  Airline: {flight['airline']}")
        print(f"  Flight Number: {flight['flight_number']}")
        print(f"  From: {flight['departure_city']} to {flight['arrival_city']}")
        print(f"  Departure: {flight['departure_time']}")
        print(f"  Arrival: {flight['arrival_time']}")
        print(f"  Price: ${flight['price']}")
        print(f"  Duration: {flight['duration']}")
        print(f"  Stops: {flight['stops']}")
        print(f"  Aircraft: {flight['aircraft']}")
        print(f"  Baggage: {flight['baggage']}")
    
    # Test hotel data
    print("\n\n=== HOTEL DATA ===")
    hotels = get_hotels("Paris", "2023-06-15", "2023-06-22", 2)
    for i, hotel in enumerate(hotels, 1):
        print(f"\nHotel {i}:")
        print(f"  Name: {hotel['hotel_name']}")
        print(f"  City: {hotel['city']}")
        print(f"  Check-in: {hotel['check_in_date']}")
        print(f"  Check-out: {hotel['check_out_date']}")
        print(f"  Price per night: ${hotel['price_per_night']}")
        print(f"  Rating: {hotel['rating']}/5")
        print(f"  Amenities: {', '.join(hotel['amenities'])}")
        print(f"  Address: {hotel['address']}")
        print(f"  Description: {hotel['description']}")
        print(f"  Room types: {', '.join(hotel['room_types'])}")
    
    # Test destination data
    print("\n\n=== DESTINATION DATA ===")
    destinations = get_destinations("beach, culture, food")
    for i, destination in enumerate(destinations, 1):
        print(f"\nDestination {i}:")
        print(f"  Name: {destination['destination']}")
        print(f"  Description: {destination['description']}")
        print(f"  Best time to visit: {destination['best_time_to_visit']}")
        print(f"  Attractions: {', '.join(destination['attractions'])}")
        print(f"  Estimated cost: {destination['estimated_cost']}")
        print(f"  Cuisine: {destination['cuisine']}")
        print(f"  Language: {destination['language']}")
        print(f"  Currency: {destination['currency']}")
        print(f"  Time zone: {destination['time_zone']}")

if __name__ == "__main__":
    main() 