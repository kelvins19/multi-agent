import asyncio
from src.agents.travel_agent import TravelAgentSystem
from src.agents.single_travel_agent import SingleTravelAgent
from src.models.base import TravelQuery
import os
import json
from typing import Dict, List, Any

async def main():
    """Main entry point for the travel agent system."""
    # Load knowledge base
    knowledge_base = load_knowledge_base()
    
    # Initialize the travel agent system
    # travel_agent = TravelAgentSystem(knowledge_base)
    travel_agent = SingleTravelAgent()
    
    print("Welcome to the Travel Agent System!")
    print("You can ask questions about flights, hotels, destinations, and general travel information.")
    print("Type 'exit' to quit.")
    
    while True:
        query = input("\nYour question: ")
        if query.lower() == "exit":
            break
        
        print("\nProcessing your query...")
        response = await travel_agent.process_query(query)
        print(f"\nResponse: {response}")

def load_knowledge_base() -> Dict[str, List[Dict[str, Any]]]:
    """Load the knowledge base from JSON files."""
    knowledge_base = {
        "flight_data": [],
        "hotel_data": [],
        "destination_data": [],
        "travel_tips": [],
        "local_attractions": []
    }
    
    # Load data from JSON files
    data_dir = "data"
    
    # Load flights data
    file_path = os.path.join(data_dir, "flights.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            flights = json.load(f)
            for flight in flights:
                knowledge_base["flight_data"].append({
                    "departure_city": flight["from"],
                    "arrival_city": flight["to"],
                    "airlines": [flight["airline"]],
                    "typical_price_range": f"${flight['price']}",
                    "flight_duration": flight["duration"]
                })
    
    # Load hotels data
    file_path = os.path.join(data_dir, "hotels.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            hotels = json.load(f)
            for hotel in hotels:
                knowledge_base["hotel_data"].append({
                    "name": hotel["name"],
                    "city": hotel["location"],
                    "rating": 4.5,  # Default rating
                    "price_range": hotel["price_range"],
                    "location": hotel["description"],
                    "amenities": ["WiFi", "Restaurant", "Room Service"]  # Default amenities
                })
    
    # Load destinations data
    file_path = os.path.join(data_dir, "attractions.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            attractions = json.load(f)
            for attraction in attractions:
                knowledge_base["destination_data"].append({
                    "destination": attraction["location"],
                    "description": attraction["description"],
                    "best_time_to_visit": "Year-round",  # Default value
                    "attractions": [attraction["name"]],
                    "estimated_cost": attraction["price_range"],
                    "activities": ["Sightseeing", "Photography", "Guided Tours"]  # Default activities
                })
    
    # Load travel tips
    file_path = os.path.join(data_dir, "activities.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            activities = json.load(f)
            for activity in activities:
                knowledge_base["travel_tips"].append({
                    "region": activity["location"],
                    "content": activity["description"]
                })
    
    # Load local attractions
    file_path = os.path.join(data_dir, "restaurants.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            restaurants = json.load(f)
            for restaurant in restaurants:
                knowledge_base["local_attractions"].append({
                    "name": restaurant["name"],
                    "region": restaurant["location"],
                    "description": restaurant["description"],
                    "location": restaurant["location"],
                    "best_time_to_visit": "Open daily"  # Default value
                })
    
    return knowledge_base

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main()) 