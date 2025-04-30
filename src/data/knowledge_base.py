"""
Knowledge base for travel information.
This file contains structured data that can be used by the travel agents.
"""

# Flight information
FLIGHT_DATA = {
    "popular_routes": [
        {
            "departure_city": "New York",
            "arrival_city": "Paris",
            "airlines": ["Air France", "Delta", "United"],
            "typical_price_range": "$500-800",
            "flight_duration": "7-8 hours"
        },
        {
            "departure_city": "London",
            "arrival_city": "Tokyo",
            "airlines": ["British Airways", "JAL", "ANA"],
            "typical_price_range": "$800-1200",
            "flight_duration": "11-12 hours"
        },
        {
            "departure_city": "San Francisco",
            "arrival_city": "Sydney",
            "airlines": ["Qantas", "United", "Air New Zealand"],
            "typical_price_range": "$900-1400",
            "flight_duration": "14-15 hours"
        }
    ],
    "airline_info": {
        "British Airways": {
            "hub": "London Heathrow",
            "alliance": "Oneworld",
            "frequent_flyer_program": "Executive Club"
        },
        "American Airlines": {
            "hub": "Dallas/Fort Worth",
            "alliance": "Oneworld",
            "frequent_flyer_program": "AAdvantage"
        },
        "Delta": {
            "hub": "Atlanta",
            "alliance": "SkyTeam",
            "frequent_flyer_program": "SkyMiles"
        },
        "Air France": {
            "hub": "Paris Charles de Gaulle",
            "alliance": "SkyTeam",
            "frequent_flyer_program": "Flying Blue"
        }
    }
}

# Hotel information
HOTEL_DATA = {
    "popular_cities": [
        {
            "city": "Paris",
            "hotels": [
                {
                    "name": "Le Grand Hotel",
                    "rating": 5,
                    "price_range": "$300-500 per night",
                    "location": "near the Eiffel Tower",
                    "amenities": ["spa", "restaurant", "pool", "fitness center"]
                },
                {
                    "name": "Boutique Marais",
                    "rating": 4,
                    "price_range": "$200-300 per night",
                    "location": "in the historic Marais district",
                    "amenities": ["breakfast included", "bar", "courtyard"]
                }
            ]
        },
        {
            "city": "Tokyo",
            "hotels": [
                {
                    "name": "Imperial Palace Hotel",
                    "rating": 5,
                    "price_range": "$400-600 per night",
                    "location": "near the Imperial Palace",
                    "amenities": ["multiple restaurants", "spa", "fitness center"]
                },
                {
                    "name": "Shibuya Crossing Hotel",
                    "rating": 4,
                    "price_range": "$250-350 per night",
                    "location": "near Shibuya Crossing",
                    "amenities": ["restaurant", "bar", "city views"]
                }
            ]
        }
    ],
    "hotel_chains": {
        "Marriott": {
            "brands": ["Ritz-Carlton", "JW Marriott", "Marriott", "Courtyard"],
            "loyalty_program": "Marriott Bonvoy"
        },
        "Hilton": {
            "brands": ["Waldorf Astoria", "Conrad", "Hilton", "DoubleTree"],
            "loyalty_program": "Hilton Honors"
        },
        "Hyatt": {
            "brands": ["Park Hyatt", "Grand Hyatt", "Hyatt Regency", "Hyatt Place"],
            "loyalty_program": "World of Hyatt"
        }
    }
}

# Destination information
DESTINATION_DATA = {
    "beach_destinations": [
        {
            "destination": "Maldives",
            "description": "Tropical paradise with crystal clear waters and luxury resorts",
            "best_time_to_visit": "November to April",
            "attractions": ["overwater bungalows", "coral reefs", "water sports"],
            "estimated_cost": "$500-1000 per day",
            "activities": ["snorkeling", "diving", "spa treatments", "island hopping"]
        },
        {
            "destination": "Bali",
            "description": "Beautiful beaches combined with rich culture and spirituality",
            "best_time_to_visit": "April to October",
            "attractions": ["Uluwatu Temple", "Nusa Dua Beach", "rice terraces"],
            "estimated_cost": "$100-300 per day",
            "activities": ["surfing", "temple visits", "yoga", "cooking classes"]
        }
    ],
    "cultural_destinations": [
        {
            "destination": "Kyoto",
            "description": "Ancient capital of Japan with stunning temples and gardens",
            "best_time_to_visit": "March-May or October-November",
            "attractions": ["Kinkaku-ji", "Fushimi Inari Shrine", "Arashiyama Bamboo Grove"],
            "estimated_cost": "$200-400 per day",
            "activities": ["tea ceremony", "temple visits", "geisha district tours"]
        },
        {
            "destination": "Rome",
            "description": "Eternal city with ancient ruins and world-class art",
            "best_time_to_visit": "April-May or September-October",
            "attractions": ["Colosseum", "Vatican Museums", "Roman Forum"],
            "estimated_cost": "$150-350 per day",
            "activities": ["historical tours", "food tours", "art gallery visits"]
        }
    ],
    "adventure_destinations": [
        {
            "destination": "New Zealand",
            "description": "Adventure sports capital with stunning natural landscapes",
            "best_time_to_visit": "December to February",
            "attractions": ["Milford Sound", "Tongariro Crossing", "Queenstown"],
            "estimated_cost": "$200-400 per day",
            "activities": ["bungee jumping", "hiking", "skiing", "skydiving"]
        },
        {
            "destination": "Costa Rica",
            "description": "Tropical paradise with rainforests and volcanoes",
            "best_time_to_visit": "December to April",
            "attractions": ["Arenal Volcano", "Manuel Antonio National Park"],
            "estimated_cost": "$100-300 per day",
            "activities": ["zip-lining", "surfing", "wildlife watching", "hiking"]
        }
    ]
}

# Travel tips by destination
TRAVEL_TIPS = {
    "Europe": [
        "Best to visit during shoulder season (April-May or September-October) for fewer crowds",
        "Get a Eurail Pass if visiting multiple countries",
        "Book museums and popular attractions in advance",
        "Learn basic phrases in local languages",
        "Be aware of pickpockets in tourist areas"
    ],
    "Asia": [
        "Consider the monsoon season when planning your trip",
        "Remove shoes when entering temples and homes",
        "Learn local customs and etiquette",
        "Try street food but ensure it's from busy vendors",
        "Get travel insurance that covers medical emergencies"
    ],
    "Australia": [
        "Summer (December-February) can be extremely hot",
        "Book Great Barrier Reef tours in advance",
        "Be prepared for long distances between cities",
        "Always use sunscreen, even on cloudy days",
        "Watch out for dangerous wildlife in remote areas"
    ]
}

# Local attractions by destination
LOCAL_ATTRACTIONS = {
    "Paris": [
        {
            "name": "Eiffel Tower",
            "description": "Iconic iron lattice tower on the Champ de Mars",
            "location": "7th arrondissement",
            "type": "landmark",
            "best_time_to_visit": "Early morning or evening"
        },
        {
            "name": "Louvre Museum",
            "description": "World's largest art museum and home to the Mona Lisa",
            "location": "1st arrondissement",
            "type": "museum",
            "best_time_to_visit": "Wednesday or Friday evening"
        }
    ],
    "Tokyo": [
        {
            "name": "Senso-ji Temple",
            "description": "Ancient Buddhist temple in Asakusa",
            "location": "Asakusa",
            "type": "temple",
            "best_time_to_visit": "Early morning"
        },
        {
            "name": "Tsukiji Outer Market",
            "description": "Famous market with fresh seafood and street food",
            "location": "Tsukiji",
            "type": "market",
            "best_time_to_visit": "Early morning for breakfast"
        }
    ],
    "New York": [
        {
            "name": "Statue of Liberty",
            "description": "Iconic symbol of freedom and democracy",
            "location": "Liberty Island",
            "type": "monument",
            "best_time_to_visit": "First ferry in the morning"
        },
        {
            "name": "Central Park",
            "description": "Massive urban park in the heart of Manhattan",
            "location": "Manhattan",
            "type": "park",
            "best_time_to_visit": "Weekday mornings"
        }
    ]
} 