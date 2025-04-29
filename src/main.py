import asyncio
from src.agents.travel_agent import TravelAgentSystem
from src.models.base import TravelQuery

async def main():
    # Initialize the travel agent system
    travel_system = TravelAgentSystem()
    
    # Example 1: Booking query
    booking_query = TravelQuery(
        text="I need to book a flight from New York to Paris on June 15, 2023",
        query_type="booking",
        metadata={"source": "user_input"}
    )
    
    print("\nProcessing booking query...")
    booking_response = await travel_system.process_query(booking_query)
    
    print(f"\nQuery: {booking_query.text}")
    print(f"Answer: {booking_response.answer}")
    
    # Example 2: Recommendation query
    recommendation_query = TravelQuery(
        text="I'm looking for a beach destination with good food and culture",
        query_type="recommendation",
        metadata={"source": "user_input"}
    )
    
    print("\nProcessing recommendation query...")
    recommendation_response = await travel_system.process_query(recommendation_query)
    
    print(f"\nQuery: {recommendation_query.text}")
    print(f"Answer: {recommendation_response.answer}")
    
    # Example 3: General query
    general_query = TravelQuery(
        text="What's the best time to visit Europe?",
        query_type="general",
        metadata={"source": "user_input"}
    )
    
    print("\nProcessing general query...")
    general_response = await travel_system.process_query(general_query)
    
    print(f"\nQuery: {general_query.text}")
    print(f"Answer: {general_response.answer}")
    
    # Print usage information
    if "usage" in general_response.metadata:
        print("\nUsage Information:")
        print(f"Total tokens: {general_response.metadata['usage'].get('total_tokens', 0)}")
        print(f"Requests: {general_response.metadata['usage'].get('requests', 0)}")

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main()) 