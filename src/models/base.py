from pydantic import BaseModel, Field
from typing import List, Dict, Any, Literal
from datetime import datetime

class Failed(BaseModel):
    """Model for failed operations."""
    reason: str = Field(..., description="The reason for the failure")

# Travel-specific models
class TravelQuery(BaseModel):
    """Travel query model."""
    text: str = Field(..., description="The travel query text")
    query_type: Literal["booking", "recommendation", "general"] = Field(..., description="Type of travel query")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata about the query")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Query creation timestamp")

class TravelResponse(BaseModel):
    """Travel response model."""
    answer: str = Field(..., description="The generated answer")
    sources: List[Dict[str, Any]] = Field(default_factory=list, description="Source documents used for the answer")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata about the response")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Response creation timestamp")

class FlightDetails(BaseModel):
    """Flight booking details."""
    flight_number: str = Field(..., description="Flight number")
    departure_city: str = Field(..., description="Departure city")
    arrival_city: str = Field(..., description="Arrival city")
    departure_time: str = Field(..., description="Departure time")
    arrival_time: str = Field(..., description="Arrival time")
    price: float = Field(..., description="Flight price")
    airline: str = Field(..., description="Airline name")

class HotelDetails(BaseModel):
    """Hotel booking details."""
    hotel_name: str = Field(..., description="Hotel name")
    city: str = Field(..., description="City where the hotel is located")
    check_in_date: str = Field(..., description="Check-in date")
    check_out_date: str = Field(..., description="Check-out date")
    price_per_night: float = Field(..., description="Price per night")
    rating: float = Field(..., description="Hotel rating")
    amenities: List[str] = Field(default_factory=list, description="Hotel amenities")

class DestinationRecommendation(BaseModel):
    """Travel destination recommendation."""
    destination: str = Field(..., description="Recommended destination")
    description: str = Field(..., description="Description of the destination")
    best_time_to_visit: str = Field(..., description="Best time to visit")
    attractions: List[str] = Field(default_factory=list, description="Popular attractions")
    estimated_cost: str = Field(..., description="Estimated cost for a trip") 