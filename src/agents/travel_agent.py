from typing import List, Dict, Any, Union, Optional, Literal
from pydantic_ai import Agent, RunContext
from pydantic_ai.usage import Usage, UsageLimits
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage

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
from src.agents.base import BaseAgent
from src.data.knowledge_base import (
    FLIGHT_DATA, 
    HOTEL_DATA, 
    DESTINATION_DATA, 
    TRAVEL_TIPS, 
    LOCAL_ATTRACTIONS
)
from src.retrievers.simple_retriever import SimpleRetriever

# Define the query classifier agent
classifier_agent = Agent[None, Union[Dict[str, Any], Failed]](
    f'openai:{settings.openai_model_name}',
    output_type=Union[Dict[str, Any], Failed],
    system_prompt=(
        "You are a query classifier for a travel agent system. "
        "Your job is to analyze travel-related queries and determine their type. "
        "There are three possible query types: 'booking', 'recommendation', or 'general'. "
        "Return a JSON object with the query_type field set to one of these values."
    ),
    base_url=settings.openai_base_url,
    api_key=settings.openai_api_key
)

# Define the booking agent for flight and hotel bookings
booking_agent = Agent[None, Union[Dict[str, Any], Failed]](
    f'openai:{settings.openai_model_name}',
    output_type=Union[Dict[str, Any], Failed],
    system_prompt=(
        "You are a travel booking agent that helps users book flights and hotels. "
        "Use the search_flights and search_hotels tools to find available options. "
        "Provide concise, direct answers based on the retrieved information. "
        "Focus on the most relevant details and avoid unnecessary verbosity."
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
        "Use the search_destinations tool to find suitable destinations. "
        "Provide concise, direct recommendations focusing on the most relevant information. "
        "Avoid unnecessary details and keep responses brief and to the point."
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
        "Use the search_travel_info tool to find relevant information. "
        "Provide concise, direct answers based on the retrieved information. "
        "Focus on answering the specific question asked without unnecessary elaboration."
    ),
    base_url=settings.openai_base_url,
    api_key=settings.openai_api_key
)

@classifier_agent.tool
async def classify_query(
    ctx: RunContext[None], 
    query_text: str
) -> Dict[str, Any]:
    """
    Classify a travel query into one of the three types: booking, recommendation, or general.
    
    Args:
        query_text: The text of the query to classify
        
    Returns:
        Dictionary with the query type
    """
    # This is a simple rule-based classifier
    query_lower = query_text.lower()
    
    # Check for booking-related keywords
    booking_keywords = ["book", "reserve", "flight", "hotel", "accommodation", "stay", "ticket", "booking", "reservation"]
    if any(keyword in query_lower for keyword in booking_keywords):
        return {"query_type": "booking"}
    
    # Check for recommendation-related keywords
    recommendation_keywords = ["recommend", "suggest", "where", "destination", "place", "visit", "go", "travel", "trip", "vacation"]
    if any(keyword in query_lower for keyword in recommendation_keywords):
        return {"query_type": "recommendation"}
    
    # Default to general
    return {"query_type": "general"}

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
    """A travel agent system that coordinates multiple specialized agents to handle different types of travel-related queries."""
    
    def __init__(self, knowledge_base: Dict[str, List[Dict[str, Any]]]):
        """Initialize the travel agent system with a knowledge base."""
        self.knowledge_base = knowledge_base
        self.retriever = SimpleRetriever(knowledge_base)
        
        # Initialize specialized agents with specific system prompts
        self.booking_agent = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        
        self.recommendation_agent = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        
        self.general_agent = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7
        )
    
    async def process_query(self, query: str) -> str:
        """Process a user query by determining its type and routing it to the appropriate handler."""
        # Determine query type based on keywords and context
        if any(keyword in query.lower() for keyword in ["book", "reserve", "schedule"]):
            return await self._handle_booking_query(query)
        elif any(keyword in query.lower() for keyword in ["recommend", "suggest", "where should"]):
            return await self._handle_recommendation_query(query)
        else:
            return await self._handle_general_query(query)
    
    async def _handle_booking_query(self, query: str) -> str:
        """Handle booking-related queries using the booking agent."""
        # Get relevant documents from the knowledge base
        relevant_docs = self.retriever.search(query, doc_type="flight")
        relevant_docs.extend(self.retriever.search(query, doc_type="hotel"))
        
        # Create context from relevant documents
        context = "\n".join([doc.content for doc in relevant_docs])
        
        # Create messages for the chat model
        messages = [
            {"role": "system", "content": "You are a travel booking assistant. Use the following context to help the user book their travel:"},
            {"role": "user", "content": f"Context:\n{context}\n\nUser query: {query}"}
        ]
        
        # Generate response
        response = await self.booking_agent.ainvoke(messages)
        return response.content
    
    async def _handle_recommendation_query(self, query: str) -> str:
        """Handle recommendation-related queries using the recommendation agent."""
        # Get relevant documents from the knowledge base
        relevant_docs = self.retriever.search(query, doc_type="destination")
        relevant_docs.extend(self.retriever.search(query, doc_type="attraction"))
        
        # Create context from relevant documents
        context = "\n".join([doc.content for doc in relevant_docs])
        
        # Create messages for the chat model
        messages = [
            {"role": "system", "content": "You are a travel recommendation assistant. Use the following context to provide personalized recommendations:"},
            {"role": "user", "content": f"Context:\n{context}\n\nUser query: {query}"}
        ]
        
        # Generate response
        response = await self.recommendation_agent.ainvoke(messages)
        return response.content
    
    async def _handle_general_query(self, query: str) -> str:
        """Handle general travel-related queries using the general agent."""
        # Get relevant documents from the knowledge base
        relevant_docs = self.retriever.search(query)
        
        # Create context from relevant documents
        context = "\n".join([doc.content for doc in relevant_docs])
        
        # Create messages for the chat model
        messages = [
            {"role": "system", "content": "You are a general travel information assistant. Use the following context to answer the user's question:"},
            {"role": "user", "content": f"Context:\n{context}\n\nUser query: {query}"}
        ]
        
        # Generate response
        response = await self.general_agent.ainvoke(messages)
        return response.content

    # Booking agent tools
    async def _book_flight(self, details: FlightDetails) -> Dict[str, Any]:
        """Book a flight with the given details."""
        # In a real system, this would call an external API or service
        return {
            "booking_id": "FL123456",
            "status": "confirmed",
            "flight_details": details.dict()
        }
    
    async def _book_hotel(self, details: HotelDetails) -> Dict[str, Any]:
        """Book a hotel with the given details."""
        # In a real system, this would call an external API or service
        return {
            "booking_id": "HT123456",
            "status": "confirmed",
            "hotel_details": details.dict()
        }
    
    async def _get_booking_status(self, booking_id: str) -> Dict[str, Any]:
        """Get the status of a booking."""
        # In a real system, this would call an external API or service
        return {
            "booking_id": booking_id,
            "status": "confirmed"
        }
    
    # Recommendation agent tools
    async def _get_destination_recommendations(self, preferences: Dict[str, Any]) -> List[DestinationRecommendation]:
        """Get destination recommendations based on user preferences."""
        # Use the retriever to find matching destinations
        relevant_docs = self.retriever.search(
            " ".join(f"{k}:{v}" for k, v in preferences.items()),
            doc_type="destination"
        )
        
        recommendations = []
        for doc in relevant_docs:
            if doc.metadata["type"] == "destination":
                dest_data = doc.metadata["destination_data"]
                recommendation = DestinationRecommendation(
                    destination=dest_data["destination"],
                    description=dest_data["description"],
                    best_time_to_visit=dest_data["best_time_to_visit"],
                    attractions=dest_data["attractions"],
                    estimated_cost=dest_data["estimated_cost"]
                )
                recommendations.append(recommendation)
        
        return recommendations
    
    async def _get_travel_tips(self, destination: str) -> List[str]:
        """Get travel tips for a specific destination."""
        # Use the retriever to find relevant tips
        relevant_docs = self.retriever.search(destination, doc_type="travel_tips")
        
        tips = []
        for doc in relevant_docs:
            if doc.metadata["type"] == "travel_tips":
                # Extract tips from the content
                doc_tips = [line.strip("- ") for line in doc.content.split("\n") if line.startswith("-")]
                tips.extend(doc_tips)
        
        return tips if tips else ["No specific tips available for this destination."]
    
    async def _get_local_attractions(self, destination: str) -> List[Dict[str, Any]]:
        """Get local attractions for a specific destination."""
        # Use the retriever to find relevant attractions
        relevant_docs = self.retriever.search(destination, doc_type="attraction")
        
        attractions = []
        for doc in relevant_docs:
            if doc.metadata["type"] == "attraction":
                attractions.append(doc.metadata["attraction_data"])
        
        return attractions if attractions else [
            {
                "name": "No attractions found",
                "description": "No specific attractions available for this destination.",
                "location": "Unknown",
                "best_time_to_visit": "Unknown"
            }
        ] 