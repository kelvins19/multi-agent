"""
Mock data for the travel agent system.
This file contains sample data for flights and hotels that can be used for testing.
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import random

# Sample flight data
MOCK_FLIGHTS = [
    {
        "flight_number": "AA123",
        "departure_city": "New York",
        "arrival_city": "Paris",
        "departure_time": "2023-06-15 10:00 AM",
        "arrival_time": "2023-06-15 12:00 PM",
        "price": 299.99,
        "airline": "American Airlines",
        "duration": "2h 0m",
        "stops": 0,
        "aircraft": "Boeing 787",
        "baggage": "1 checked bag included"
    },
    {
        "flight_number": "UA456",
        "departure_city": "New York",
        "arrival_city": "Paris",
        "departure_time": "2023-06-15 2:00 PM",
        "arrival_time": "2023-06-15 4:00 PM",
        "price": 349.99,
        "airline": "United Airlines",
        "duration": "2h 0m",
        "stops": 0,
        "aircraft": "Airbus A350",
        "baggage": "1 checked bag included"
    },
    {
        "flight_number": "DL789",
        "departure_city": "New York",
        "arrival_city": "Paris",
        "departure_time": "2023-06-15 7:00 PM",
        "arrival_time": "2023-06-16 9:00 AM",
        "price": 249.99,
        "airline": "Delta Airlines",
        "duration": "14h 0m",
        "stops": 1,
        "aircraft": "Boeing 777",
        "baggage": "1 checked bag included"
    },
    {
        "flight_number": "AF101",
        "departure_city": "New York",
        "arrival_city": "Paris",
        "departure_time": "2023-06-15 11:30 PM",
        "arrival_time": "2023-06-16 1:30 PM",
        "price": 279.99,
        "airline": "Air France",
        "duration": "14h 0m",
        "stops": 0,
        "aircraft": "Airbus A380",
        "baggage": "1 checked bag included"
    },
    {
        "flight_number": "BA202",
        "departure_city": "New York",
        "arrival_city": "Paris",
        "departure_time": "2023-06-15 8:00 AM",
        "arrival_time": "2023-06-15 8:00 PM",
        "price": 229.99,
        "airline": "British Airways",
        "duration": "12h 0m",
        "stops": 1,
        "aircraft": "Boeing 747",
        "baggage": "1 checked bag included"
    }
]

# Sample hotel data
MOCK_HOTELS = [
    {
        "hotel_name": "Grand Hotel Paris",
        "city": "Paris",
        "check_in_date": "2023-06-15",
        "check_out_date": "2023-06-22",
        "price_per_night": 199.99,
        "rating": 4.5,
        "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Room Service", "Gym"],
        "address": "123 Champs-Élysées, Paris, France",
        "description": "Luxury hotel in the heart of Paris with stunning views of the Eiffel Tower.",
        "room_types": ["Standard", "Deluxe", "Suite"],
        "images": ["https://example.com/grand-hotel-1.jpg", "https://example.com/grand-hotel-2.jpg"]
    },
    {
        "hotel_name": "Le Petit Hotel",
        "city": "Paris",
        "check_in_date": "2023-06-15",
        "check_out_date": "2023-06-22",
        "price_per_night": 149.99,
        "rating": 3.8,
        "amenities": ["WiFi", "Breakfast", "Gym"],
        "address": "45 Rue de Rivoli, Paris, France",
        "description": "Charming boutique hotel in a historic building near the Louvre.",
        "room_types": ["Standard", "Superior"],
        "images": ["https://example.com/petit-hotel-1.jpg", "https://example.com/petit-hotel-2.jpg"]
    },
    {
        "hotel_name": "Paris Luxury Suites",
        "city": "Paris",
        "check_in_date": "2023-06-15",
        "check_out_date": "2023-06-22",
        "price_per_night": 299.99,
        "rating": 4.9,
        "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Room Service", "Gym", "Concierge", "Valet Parking"],
        "address": "78 Avenue Montaigne, Paris, France",
        "description": "Ultimate luxury experience with personalized service and exclusive amenities.",
        "room_types": ["Deluxe", "Suite", "Presidential Suite"],
        "images": ["https://example.com/luxury-suites-1.jpg", "https://example.com/luxury-suites-2.jpg"]
    },
    {
        "hotel_name": "Eiffel View Hotel",
        "city": "Paris",
        "check_in_date": "2023-06-15",
        "check_out_date": "2023-06-22",
        "price_per_night": 249.99,
        "rating": 4.2,
        "amenities": ["WiFi", "Restaurant", "Bar", "Terrace", "Room Service"],
        "address": "15 Avenue de la Bourdonnais, Paris, France",
        "description": "Modern hotel with spectacular views of the Eiffel Tower from most rooms.",
        "room_types": ["Standard", "Deluxe", "Eiffel View Suite"],
        "images": ["https://example.com/eiffel-view-1.jpg", "https://example.com/eiffel-view-2.jpg"]
    },
    {
        "hotel_name": "Budget Inn Paris",
        "city": "Paris",
        "check_in_date": "2023-06-15",
        "check_out_date": "2023-06-22",
        "price_per_night": 99.99,
        "rating": 3.2,
        "amenities": ["WiFi", "Breakfast"],
        "address": "32 Rue de la Roquette, Paris, France",
        "description": "Affordable accommodation in a vibrant neighborhood with easy access to public transport.",
        "room_types": ["Standard", "Twin"],
        "images": ["https://example.com/budget-inn-1.jpg", "https://example.com/budget-inn-2.jpg"]
    }
]

# Sample destination recommendations
MOCK_DESTINATIONS = [
    {
        "destination": "Paris, France",
        "description": "The City of Light, known for its art, fashion, gastronomy, and culture. Home to iconic landmarks like the Eiffel Tower, Louvre Museum, and Notre-Dame Cathedral.",
        "best_time_to_visit": "April to June, September to October",
        "attractions": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral", "Champs-Élysées", "Arc de Triomphe", "Seine River", "Montmartre", "Palace of Versailles"],
        "estimated_cost": "$2,000 - $3,000 for a week",
        "cuisine": "French cuisine, known for pastries, wine, and fine dining",
        "language": "French",
        "currency": "Euro (EUR)",
        "time_zone": "CET (UTC+1)",
        "images": ["https://example.com/paris-1.jpg", "https://example.com/paris-2.jpg"]
    },
    {
        "destination": "Bali, Indonesia",
        "description": "A tropical paradise with beautiful beaches, lush landscapes, and rich culture. Known for its stunning rice terraces, ancient temples, and vibrant arts scene.",
        "best_time_to_visit": "April to October",
        "attractions": ["Ubud", "Seminyak Beach", "Mount Batur", "Rice Terraces", "Uluwatu Temple", "Nusa Dua", "Gili Islands", "Water Temples"],
        "estimated_cost": "$1,500 - $2,500 for a week",
        "cuisine": "Balinese cuisine, known for spices, rice dishes, and fresh seafood",
        "language": "Indonesian and Balinese",
        "currency": "Indonesian Rupiah (IDR)",
        "time_zone": "Central Indonesian Time (WITA, UTC+8)",
        "images": ["https://example.com/bali-1.jpg", "https://example.com/bali-2.jpg"]
    },
    {
        "destination": "Tokyo, Japan",
        "description": "A fascinating blend of the ultramodern and traditional, from neon-lit skyscrapers to historic temples. Known for its pop culture, fashion, and culinary scene.",
        "best_time_to_visit": "March to May, September to November",
        "attractions": ["Shibuya Crossing", "Senso-ji Temple", "Tokyo Skytree", "Tsukiji Outer Market", "Shinjuku Gyoen", "Harajuku", "Akihabara", "Imperial Palace"],
        "estimated_cost": "$2,500 - $3,500 for a week",
        "cuisine": "Japanese cuisine, known for sushi, ramen, and tempura",
        "language": "Japanese",
        "currency": "Japanese Yen (JPY)",
        "time_zone": "Japan Standard Time (JST, UTC+9)",
        "images": ["https://example.com/tokyo-1.jpg", "https://example.com/tokyo-2.jpg"]
    },
    {
        "destination": "New York City, USA",
        "description": "The city that never sleeps, offering world-class museums, theaters, restaurants, and shopping. Known for its iconic skyline, diverse neighborhoods, and vibrant energy.",
        "best_time_to_visit": "April to June, September to November",
        "attractions": ["Times Square", "Central Park", "Statue of Liberty", "Empire State Building", "Metropolitan Museum of Art", "Brooklyn Bridge", "Fifth Avenue", "Broadway"],
        "estimated_cost": "$2,000 - $3,000 for a week",
        "cuisine": "Diverse international cuisine, known for pizza, bagels, and street food",
        "language": "English",
        "currency": "US Dollar (USD)",
        "time_zone": "Eastern Time (ET, UTC-5)",
        "images": ["https://example.com/nyc-1.jpg", "https://example.com/nyc-2.jpg"]
    },
    {
        "destination": "Santorini, Greece",
        "description": "A stunning island in the Aegean Sea, known for its white-washed buildings, blue-domed churches, and breathtaking sunsets. Famous for its volcanic beaches and wine.",
        "best_time_to_visit": "May to October",
        "attractions": ["Oia", "Fira", "Red Beach", "Santorini Wine Museum", "Akrotiri Archaeological Site", "Santorini Caldera", "Black Beach", "Santorini Volcano"],
        "estimated_cost": "$1,800 - $2,800 for a week",
        "cuisine": "Greek cuisine, known for fresh seafood, olives, and feta cheese",
        "language": "Greek",
        "currency": "Euro (EUR)",
        "time_zone": "Eastern European Time (EET, UTC+2)",
        "images": ["https://example.com/santorini-1.jpg", "https://example.com/santorini-2.jpg"]
    }
]

def get_flights(departure_city: str, arrival_city: str, departure_date: str) -> List[Dict[str, Any]]:
    """
    Get mock flight data based on search criteria.
    
    Args:
        departure_city: City of departure
        arrival_city: City of arrival
        departure_date: Date of departure
        
    Returns:
        List of available flights
    """
    # In a real implementation, this would filter based on the search criteria
    # For mock data, we'll just return all flights
    return MOCK_FLIGHTS

def get_hotels(city: str, check_in_date: str, check_out_date: str, guests: int = 2) -> List[Dict[str, Any]]:
    """
    Get mock hotel data based on search criteria.
    
    Args:
        city: City to search in
        check_in_date: Check-in date
        check_out_date: Check-out date
        guests: Number of guests
        
    Returns:
        List of available hotels
    """
    # In a real implementation, this would filter based on the search criteria
    # For mock data, we'll just return all hotels
    return MOCK_HOTELS

def get_destinations(preferences: str) -> List[Dict[str, Any]]:
    """
    Get mock destination recommendations based on preferences.
    
    Args:
        preferences: User preferences for destinations
        
    Returns:
        List of recommended destinations
    """
    # In a real implementation, this would filter based on the preferences
    # For mock data, we'll just return all destinations
    return MOCK_DESTINATIONS 