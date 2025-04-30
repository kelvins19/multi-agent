"""Base models for the travel system."""
from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel

class TravelQuery(BaseModel):
    """A travel-related query."""
    text: str
    query_type: Optional[str] = None  # "booking", "recommendation", or "general"
    metadata: Dict[str, Any] = {}

class FlightDetails(BaseModel):
    """Details for a flight booking."""
    flight_number: str
    departure_city: str
    arrival_city: str
    departure_time: str
    arrival_time: str
    price: float
    airline: str

class HotelDetails(BaseModel):
    """Details for a hotel booking."""
    hotel_name: str
    city: str
    check_in_date: str
    check_out_date: str
    price_per_night: float
    rating: float
    amenities: List[str]

class DestinationRecommendation(BaseModel):
    """A destination recommendation."""
    destination: str
    description: str
    best_time_to_visit: str
    attractions: List[str]
    estimated_cost: str

class Failed(BaseModel):
    """A failed response."""
    error: str
    details: Dict[str, Any] = {}

class TravelResponse(BaseModel):
    """A response to a travel query."""
    answer: str
    sources: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = {} 