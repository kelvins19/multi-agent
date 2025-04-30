from typing import List, Dict, Any, Union, Optional, Literal
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.usage import Usage, UsageLimits
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from langsmith import traceable
from langsmith.wrappers import wrap_openai

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

class TravelDeps(BaseModel):
    """Dependencies for the travel agent system."""
    query: str
    query_type: Optional[str] = None

class TravelAgentSystem:
    """A travel agent system that coordinates multiple specialized agents to handle different types of travel-related queries."""
    
    def __init__(self, knowledge_base: Dict[str, List[Dict[str, Any]]]):
        """Initialize the travel agent system with a knowledge base."""
        self.knowledge_base = knowledge_base
        self.retriever = SimpleRetriever(knowledge_base)
        
        # Initialize the OpenAI model
        os.environ["OPENAI_API_KEY"] = settings.openai_api_key
        self.model = OpenAIModel(
            model_name="gpt-4o-mini",
        )
        
        # Initialize specialized agents
        self.booking_agent = Agent(
            self.model,
            system_prompt=(
                "You are a travel booking agent that helps users book flights and hotels. "
                "Use the search_flights and search_hotels tools to find available options. "
                "Provide concise, direct answers based on the retrieved information. "
                "Focus on the most relevant details and avoid unnecessary verbosity."
            ),
            deps_type=TravelDeps
        )
        
        self.recommendation_agent = Agent(
            self.model,
            system_prompt=(
                "You are a travel recommendation agent that suggests destinations based on user preferences. "
                "Use the search_destinations tool to find suitable destinations. "
                "Provide concise, direct recommendations focusing on the most relevant information. "
                "Avoid unnecessary details and keep responses brief and to the point."
            ),
            deps_type=TravelDeps
        )
        
        self.general_agent = Agent(
            self.model,
            system_prompt=(
                "You are a general travel assistant that answers questions about travel. "
                "Use the search_travel_info tool to find relevant information. "
                "Provide concise, direct answers based on the retrieved information. "
                "Focus on answering the specific question asked without unnecessary elaboration."
            ),
            deps_type=TravelDeps
        )
        
        # Register tools for each agent
        self.booking_agent.tool(self._search_flights)
        self.booking_agent.tool(self._search_hotels)
        self.recommendation_agent.tool(self._search_destinations)
        self.general_agent.tool(self._search_travel_info)
    
    @traceable(run_type="chain", name="Process Travel Query")
    async def process_query(self, query: str) -> str:
        """Process a user query by determining its type and routing it to the appropriate handler."""
        # Determine query type based on keywords and context
        if any(keyword in query.lower() for keyword in ["book", "reserve", "schedule"]):
            return await self._handle_booking_query(query)
        elif any(keyword in query.lower() for keyword in ["recommend", "suggest", "where should"]):
            return await self._handle_recommendation_query(query)
        else:
            return await self._handle_general_query(query)
    
    @traceable(run_type="chain", name="Handle Booking Query")
    async def _handle_booking_query(self, query: str) -> str:
        """Handle booking-related queries using the booking agent."""
        deps = TravelDeps(query=query, query_type="booking")
        result = await self.booking_agent.run(user_prompt=query, deps=deps)
        
        if result is None:
            return "I apologize, but I couldn't process your booking request at this time."
            
        usage = result.usage()
        if usage is not None:
            print(f"\nToken Usage for Booking Query:")
            print(f"Input Tokens: {usage.request_tokens}")
            print(f"Output Tokens: {usage.response_tokens}")
            print(f"Total Tokens: {usage.total_tokens}")
            
        return result.data
    
    @traceable(run_type="chain", name="Handle Recommendation Query")
    async def _handle_recommendation_query(self, query: str) -> str:
        """Handle recommendation-related queries using the recommendation agent."""
        deps = TravelDeps(query=query, query_type="recommendation")
        result = await self.recommendation_agent.run(user_prompt=query, deps=deps)
        
        if result is None:
            return "I apologize, but I couldn't process your recommendation request at this time."
            
        usage = result.usage()
        if usage is not None:
            print(f"\nToken Usage for Recommendation Query:")
            print(f"Input Tokens: {usage.request_tokens}")
            print(f"Output Tokens: {usage.response_tokens}")
            print(f"Total Tokens: {usage.total_tokens}")
            
        return result.data
    
    @traceable(run_type="chain", name="Handle General Query")
    async def _handle_general_query(self, query: str) -> str:
        """Handle general travel-related queries using the general agent."""
        deps = TravelDeps(query=query, query_type="general")
        result = await self.general_agent.run(user_prompt=query, deps=deps)
        
        if result is None:
            return "I apologize, but I couldn't process your query at this time."
            
        usage = result.usage()
        if usage is not None:
            print(f"\nToken Usage for General Query:")
            print(f"Input Tokens: {usage.request_tokens}")
            print(f"Output Tokens: {usage.response_tokens}")
            print(f"Total Tokens: {usage.total_tokens}")
            
        return result.data

    @traceable(run_type="tool", name="Search Flights")
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

    @traceable(run_type="tool", name="Search Hotels")
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

    @traceable(run_type="tool", name="Search Destinations")
    async def _search_destinations(
        self,
        ctx: RunContext[TravelDeps], 
        preferences: str
    ) -> List[DestinationRecommendation]:
        """Search for travel destinations based on preferences."""
        destinations_data = get_destinations(preferences)
        return [DestinationRecommendation(**dest_data) for dest_data in destinations_data]

    @traceable(run_type="tool", name="Search Travel Info")
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