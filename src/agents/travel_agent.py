from typing import List, Dict, Any, Union, Optional, Literal
from pydantic_ai import Agent, RunContext
from pydantic_ai.usage import Usage, UsageLimits

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

# Define the booking agent for flight and hotel bookings
booking_agent = Agent[None, Union[Dict[str, Any], Failed]](
    f'openai:{settings.openai_model_name}',
    output_type=Union[Dict[str, Any], Failed],
    system_prompt=(
        "You are a travel booking agent that helps users book flights and hotels. "
        "Use the search_flights and search_hotels tools to find available options."
    ),
    base_url=settings.openai_base_url,
    api_key=settings.openai_api_key
)

# Define the recommendation agent for travel destinations
recommendation_agent = Agent[None, Union[DestinationRecommendation, Failed]](
    f'openai:{settings.openai_model_name}',
    output_type=Union[DestinationRecommendation, Failed],
    system_prompt=(
        "You are a travel recommendation agent that suggests destinations based on user preferences. "
        "Use the search_destinations tool to find suitable destinations."
    ),
    base_url=settings.openai_base_url,
    api_key=settings.openai_api_key
)

# Define the general inquiry agent for other travel questions
general_agent = Agent[None, Union[TravelResponse, Failed]](
    f'openai:{settings.openai_model_name}',
    output_type=Union[TravelResponse, Failed],
    system_prompt=(
        "You are a general travel assistant that answers questions about travel. "
        "Use the search_travel_info tool to find relevant information."
    ),
    base_url=settings.openai_base_url,
    api_key=settings.openai_api_key
)

@booking_agent.tool
async def search_flights(
    ctx: RunContext[None], 
    departure_city: str, 
    arrival_city: str, 
    departure_date: str
) -> List[FlightDetails]:
    """
    Search for available flights.
    
    Args:
        departure_city: City of departure
        arrival_city: City of arrival
        departure_date: Date of departure
        
    Returns:
        List of available flights
    """
    # Use the mock data function to get flights
    flights_data = get_flights(departure_city, arrival_city, departure_date)
    
    # Convert the dictionary data to FlightDetails objects
    flights = []
    for flight_data in flights_data:
        flight = FlightDetails(
            flight_number=flight_data["flight_number"],
            departure_city=flight_data["departure_city"],
            arrival_city=flight_data["arrival_city"],
            departure_time=flight_data["departure_time"],
            arrival_time=flight_data["arrival_time"],
            price=flight_data["price"],
            airline=flight_data["airline"]
        )
        flights.append(flight)
    
    return flights

@booking_agent.tool
async def search_hotels(
    ctx: RunContext[None], 
    city: str, 
    check_in_date: str, 
    check_out_date: str,
    guests: int = 2
) -> List[HotelDetails]:
    """
    Search for available hotels.
    
    Args:
        city: City to search in
        check_in_date: Check-in date
        check_out_date: Check-out date
        guests: Number of guests
        
    Returns:
        List of available hotels
    """
    # Use the mock data function to get hotels
    hotels_data = get_hotels(city, check_in_date, check_out_date, guests)
    
    # Convert the dictionary data to HotelDetails objects
    hotels = []
    for hotel_data in hotels_data:
        hotel = HotelDetails(
            hotel_name=hotel_data["hotel_name"],
            city=hotel_data["city"],
            check_in_date=hotel_data["check_in_date"],
            check_out_date=hotel_data["check_out_date"],
            price_per_night=hotel_data["price_per_night"],
            rating=hotel_data["rating"],
            amenities=hotel_data["amenities"]
        )
        hotels.append(hotel)
    
    return hotels

@recommendation_agent.tool
async def search_destinations(
    ctx: RunContext[None], 
    preferences: str
) -> List[DestinationRecommendation]:
    """
    Search for travel destinations based on preferences.
    
    Args:
        preferences: User preferences for destinations
        
    Returns:
        List of recommended destinations
    """
    # Use the mock data function to get destinations
    destinations_data = get_destinations(preferences)
    
    # Convert the dictionary data to DestinationRecommendation objects
    destinations = []
    for dest_data in destinations_data:
        destination = DestinationRecommendation(
            destination=dest_data["destination"],
            description=dest_data["description"],
            best_time_to_visit=dest_data["best_time_to_visit"],
            attractions=dest_data["attractions"],
            estimated_cost=dest_data["estimated_cost"]
        )
        destinations.append(destination)
    
    return destinations

@general_agent.tool
async def search_travel_info(
    ctx: RunContext[None], 
    query: str
) -> Dict[str, Any]:
    """
    Search for general travel information.
    
    Args:
        query: The search query
        
    Returns:
        Dictionary with travel information
    """
    # Return a sample response for now
    return {
        "content": "This is a sample response about travel information.",
        "metadata": {"source": "sample", "relevance": 0.95}
    }

class TravelAgentSystem:
    """Travel agent system with specialized agents for different tasks."""
    
    def __init__(self):
        self.usage_limits = UsageLimits(request_limit=10, total_tokens_limit=4000)
    
    async def process_query(self, query: TravelQuery) -> TravelResponse:
        """
        Process a travel query through the appropriate agent.
        
        Args:
            query: The travel query to process
            
        Returns:
            A travel response containing the answer and metadata
        """
        usage = Usage()
        
        if query.query_type == "booking":
            # Process booking query
            booking_result = await booking_agent.run(
                query.text,
                usage=usage,
                usage_limits=self.usage_limits
            )
            
            if isinstance(booking_result.output, Failed):
                return TravelResponse(
                    answer=f"Failed to process booking: {booking_result.output.reason}",
                    sources=[],
                    metadata={"error": "booking_failed"}
                )
            
            # Format the booking details into a response
            booking_details = booking_result.output
            answer = self._format_booking_response(booking_details)
            
            return TravelResponse(
                answer=answer,
                sources=[],
                metadata={"booking_details": booking_details, "usage": {"total_tokens": usage.total_tokens, "requests": usage.requests}}
            )
            
        elif query.query_type == "recommendation":
            # Process recommendation query
            recommendation_result = await recommendation_agent.run(
                query.text,
                usage=usage,
                usage_limits=self.usage_limits
            )
            
            if isinstance(recommendation_result.output, Failed):
                return TravelResponse(
                    answer=f"Failed to process recommendation: {recommendation_result.output.reason}",
                    sources=[],
                    metadata={"error": "recommendation_failed"}
                )
            
            # Format the recommendation into a response
            recommendation = recommendation_result.output
            answer = self._format_recommendation_response(recommendation)
            
            return TravelResponse(
                answer=answer,
                sources=[],
                metadata={"recommendation": recommendation.model_dump(), "usage": {"total_tokens": usage.total_tokens, "requests": usage.requests}}
            )
            
        else:  # general query
            # Process general query
            general_result = await general_agent.run(
                query.text,
                usage=usage,
                usage_limits=self.usage_limits
            )
            
            if isinstance(general_result.output, Failed):
                return TravelResponse(
                    answer=f"Failed to process query: {general_result.output.reason}",
                    sources=[],
                    metadata={"error": "query_failed"}
                )
            
            return TravelResponse(
                answer=general_result.output.answer,
                sources=[],
                metadata={"usage": {"total_tokens": usage.total_tokens, "requests": usage.requests}}
            )
    
    def _format_booking_response(self, booking_details: Dict[str, Any]) -> str:
        """Format booking details into a readable response."""
        if "flights" in booking_details:
            flights = booking_details["flights"]
            return f"Found {len(flights)} flights matching your criteria."
        elif "hotels" in booking_details:
            hotels = booking_details["hotels"]
            return f"Found {len(hotels)} hotels matching your criteria."
        else:
            return "No booking details found."
    
    def _format_recommendation_response(self, recommendation: DestinationRecommendation) -> str:
        """Format destination recommendation into a readable response."""
        return (
            f"I recommend {recommendation.destination}. "
            f"{recommendation.description}\n"
            f"Best time to visit: {recommendation.best_time_to_visit}\n"
            f"Top attractions: {', '.join(recommendation.attractions)}\n"
            f"Estimated cost: ${recommendation.estimated_cost}"
        ) 