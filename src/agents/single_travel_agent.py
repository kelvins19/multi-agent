from typing import List, Dict, Any, Optional
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.usage import Usage, UsageLimits
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from langsmith import traceable

from src.models.base import (
    TravelQuery, 
    TravelResponse, 
    Failed,
    FlightDetails,
    HotelDetails,
    DestinationRecommendation
)
from src.config import settings
from src.data.mock_data import get_flights, get_hotels, get_destinations
from src.data.knowledge_base import (
    FLIGHT_DATA, 
    HOTEL_DATA, 
    DESTINATION_DATA, 
    TRAVEL_TIPS, 
    LOCAL_ATTRACTIONS
)

class TravelDeps(BaseModel):
    """Dependencies for the travel agent."""
    query: str
    query_type: Optional[str] = None

class SingleTravelAgent:
    """A single travel agent that handles all travel-related queries."""
    
    def __init__(self):
        """Initialize the travel agent with necessary components."""
        # Initialize the OpenAI model
        os.environ["OPENAI_API_KEY"] = settings.openai_api_key
        self.model = OpenAIModel(
            model_name="gpt-4o-mini",
        )
        
        # Initialize the main agent
        self.agent = Agent(
            self.model,
            system_prompt=(
                "You are a comprehensive travel assistant that can handle all types of travel-related queries. "
                "You can help with booking flights and hotels, recommending destinations, and providing general travel information. "
                "Use the available tools to search for information and provide accurate, helpful responses. "
                "Keep your responses concise and focused on the user's specific needs."
            ),
            deps_type=TravelDeps
        )
        
        # Initialize message history
        self.message_history = []
        
        # Register all tools
        self.agent.tool(self._search_flights)
        self.agent.tool(self._search_hotels)
        self.agent.tool(self._search_destinations)
        self.agent.tool(self._search_travel_info)
        self.agent.tool(self._book_flight)
        self.agent.tool(self._book_hotel)
        self.agent.tool(self._get_booking_status)
        self.agent.tool(self._get_travel_tips)
        self.agent.tool(self._get_local_attractions)
    
    @traceable(run_type="chain", name="Single -- Process Travel Query")
    async def process_query(self, query: str) -> str:
        """Process any travel-related query using the single agent."""
        deps = TravelDeps(query=query)
        result = await self.agent.run(
            user_prompt=query, 
            deps=deps,
            message_history=self.message_history
        )
        
        if result is None:
            return "I apologize, but I couldn't process your request at this time."
            
        # Update message history with new messages
        self.message_history.extend(result.new_messages())
            
        usage = result.usage()
        if usage is not None:
            print(f"\nToken Usage:")
            print(f"Input Tokens: {usage.request_tokens}")
            print(f"Output Tokens: {usage.response_tokens}")
            print(f"Total Tokens: {usage.total_tokens}")
            
            # Return a new response object with token usage
            return {
                "choices": [{"message": {"role": "assistant", "content": result.data}}],
                "usage_metadata": {
                    "input_tokens": usage.request_tokens,
                    "output_tokens": usage.response_tokens,
                    "total_tokens": usage.total_tokens
                }
            }
            
        return result.data

    @traceable(run_type="tool", name="Single -- Search Flights")
    async def _search_flights(
        self,
        ctx: RunContext[TravelDeps], 
        departure_city: str, 
        arrival_city: str, 
        departure_date: str
    ) -> List[FlightDetails]:
        """Search for available flights."""
        flights_data = get_flights(departure_city, arrival_city, departure_date)
        return [FlightDetails(**flight_data) for flight_data in flights_data]

    @traceable(run_type="tool", name="Single -- Search Hotels")
    async def _search_hotels(
        self,
        ctx: RunContext[TravelDeps], 
        city: str, 
        check_in_date: str, 
        check_out_date: str,
        guests: int = 2
    ) -> List[HotelDetails]:
        """Search for available hotels."""
        hotels_data = get_hotels(city, check_in_date, check_out_date, guests)
        return [HotelDetails(**hotel_data) for hotel_data in hotels_data]

    @traceable(run_type="tool", name="Single -- Search Destinations")
    async def _search_destinations(
        self,
        ctx: RunContext[TravelDeps], 
        preferences: str
    ) -> List[DestinationRecommendation]:
        """Search for travel destinations based on preferences."""
        destinations_data = get_destinations(preferences)
        return [DestinationRecommendation(**dest_data) for dest_data in destinations_data]

    @traceable(run_type="tool", name="Single -- Search Travel Info")
    async def _search_travel_info(
        self,
        ctx: RunContext[TravelDeps], 
        query: str
    ) -> Dict[str, Any]:
        """Search for general travel information."""
        return {
            "content": "This is a sample response about travel information.",
            "metadata": {"source": "sample", "relevance": 0.95}
        }

    @traceable(run_type="tool", name="Single -- Book Flight")
    async def _book_flight(
        self,
        ctx: RunContext[TravelDeps],
        details: FlightDetails
    ) -> Dict[str, Any]:
        """Book a flight with the given details."""
        return {
            "booking_id": "FL123456",
            "status": "confirmed",
            "flight_details": details.dict()
        }
    
    @traceable(run_type="tool", name="Single -- Book Hotel")
    async def _book_hotel(
        self,
        ctx: RunContext[TravelDeps],
        details: HotelDetails
    ) -> Dict[str, Any]:
        """Book a hotel with the given details."""
        return {
            "booking_id": "HT123456",
            "status": "confirmed",
            "hotel_details": details.dict()
        }
    
    @traceable(run_type="tool", name="Single -- Get Booking Status")
    async def _get_booking_status(
        self,
        ctx: RunContext[TravelDeps],
        booking_id: str
    ) -> Dict[str, Any]:
        """Get the status of a booking."""
        return {
            "booking_id": booking_id,
            "status": "confirmed"
        }
    
    @traceable(run_type="tool", name="Single -- Get Travel Tips")
    async def _get_travel_tips(
        self,
        ctx: RunContext[TravelDeps],
        destination: str
    ) -> List[str]:
        """Get travel tips for a specific destination."""
        tips = TRAVEL_TIPS.get(destination, [])
        return tips if tips else ["No specific tips available for this destination."]
    
    @traceable(run_type="tool", name="Single -- Get Local Attractions")
    async def _get_local_attractions(
        self,
        ctx: RunContext[TravelDeps],
        destination: str
    ) -> List[Dict[str, Any]]:
        """Get local attractions for a specific destination."""
        attractions = LOCAL_ATTRACTIONS.get(destination, [])
        return attractions if attractions else [
            {
                "name": "No attractions found",
                "description": "No specific attractions available for this destination.",
                "location": "Unknown",
                "best_time_to_visit": "Unknown"
            }
        ] 