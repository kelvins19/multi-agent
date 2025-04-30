from typing import List, Dict, Any, Optional
from src.data.knowledge_base import (
    FLIGHT_DATA, 
    HOTEL_DATA, 
    DESTINATION_DATA, 
    TRAVEL_TIPS, 
    LOCAL_ATTRACTIONS
)

class Document:
    """Simple document class to store content and metadata."""
    def __init__(self, content: str, metadata: Dict[str, Any] = None):
        self.content = content
        self.metadata = metadata or {}

class SimpleRetriever:
    """A simple retriever that uses basic text matching to find relevant documents."""
    
    def __init__(self, knowledge_base: Dict[str, List[Dict[str, Any]]] = None):
        """Initialize the retriever with a knowledge base."""
        self.knowledge_base = knowledge_base or {}
        self.documents = self._initialize_documents()
    
    def _initialize_documents(self) -> List[Document]:
        """Initialize documents from the knowledge base."""
        documents = []
        
        # Process flight data
        for route in self.knowledge_base.get("flight_data", []):
            content = f"Flight from {route['departure_city']} to {route['arrival_city']}. "
            content += f"Airlines: {', '.join(route['airlines'])}. "
            content += f"Typical price range: {route['typical_price_range']}. "
            content += f"Flight duration: {route['flight_duration']}."
            
            documents.append(Document(
                content=content,
                metadata={
                    "type": "flight",
                    "departure_city": route["departure_city"],
                    "arrival_city": route["arrival_city"],
                    "route_data": route
                }
            ))
        
        # Process hotel data
        for hotel in self.knowledge_base.get("hotel_data", []):
            content = f"Hotel: {hotel['name']} in {hotel['city']}. "
            content += f"Rating: {hotel['rating']} stars. "
            content += f"Price range: {hotel['price_range']}. "
            content += f"Location: {hotel['location']}. "
            content += f"Amenities: {', '.join(hotel['amenities'])}."
            
            documents.append(Document(
                content=content,
                metadata={
                    "type": "hotel",
                    "city": hotel["city"],
                    "hotel_data": hotel
                }
            ))
        
        # Process destination data
        for dest in self.knowledge_base.get("destination_data", []):
            content = f"Destination: {dest['destination']}. "
            content += f"Description: {dest['description']}. "
            content += f"Best time to visit: {dest['best_time_to_visit']}. "
            content += f"Estimated cost: {dest['estimated_cost']}. "
            content += f"Popular activities: {', '.join(dest['activities'])}. "
            content += f"Top attractions: {', '.join(dest['attractions'])}."
            
            documents.append(Document(
                content=content,
                metadata={
                    "type": "destination",
                    "destination_data": dest
                }
            ))
        
        # Process travel tips
        for tip in self.knowledge_base.get("travel_tips", []):
            content = f"Travel tip for {tip['region']}: {tip['content']}"
            
            documents.append(Document(
                content=content,
                metadata={
                    "type": "travel_tips",
                    "region": tip["region"],
                    "tip_data": tip
                }
            ))
        
        # Process local attractions
        for attraction in self.knowledge_base.get("local_attractions", []):
            content = f"Attraction: {attraction['name']} in {attraction['region']}. "
            content += f"Description: {attraction['description']}. "
            content += f"Location: {attraction['location']}. "
            content += f"Best time to visit: {attraction['best_time_to_visit']}."
            
            documents.append(Document(
                content=content,
                metadata={
                    "type": "attraction",
                    "region": attraction["region"],
                    "attraction_data": attraction
                }
            ))
        
        return documents
    
    def search(self, query: str, doc_type: Optional[str] = None, top_k: int = 5) -> List[Document]:
        """Search for relevant documents based on the query."""
        query_terms = query.lower().split()
        scored_docs = []
        
        for doc in self.documents:
            # Skip documents of different type if doc_type is specified
            if doc_type and doc.metadata["type"] != doc_type:
                continue
            
            score = 0.0
            doc_content = doc.content.lower()
            
            # Check for exact phrase matches (higher weight)
            if query.lower() in doc_content:
                score += 2.0
            
            # Check for individual term matches
            for term in query_terms:
                if term in doc_content:
                    # Count occurrences for term frequency
                    term_count = doc_content.count(term)
                    score += 0.5 * term_count
            
            # Apply metadata-specific boosts
            if doc.metadata["type"] == "flight" and any(term in ["flight", "fly", "airplane", "airline"] for term in query_terms):
                score += 1.0
            elif doc.metadata["type"] == "hotel" and any(term in ["hotel", "stay", "accommodation", "room"] for term in query_terms):
                score += 1.0
            elif doc.metadata["type"] == "destination" and any(term in ["destination", "place", "location", "city", "country"] for term in query_terms):
                score += 1.0
            elif doc.metadata["type"] == "attraction" and any(term in ["attraction", "see", "visit", "sight", "place"] for term in query_terms):
                score += 1.0
            elif doc.metadata["type"] == "travel_tips" and any(term in ["tip", "advice", "recommendation", "suggestion"] for term in query_terms):
                score += 1.0
            
            # Add document if it has a non-zero score
            if score > 0:
                scored_docs.append((score, doc))
        
        # Sort by score in descending order
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        
        # Return top k documents
        return [doc for _, doc in scored_docs[:top_k]] 