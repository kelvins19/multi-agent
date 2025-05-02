# Travel Agent Systems Documentation

This document explains the architecture and functionality of two different travel agent systems: the Multi-Agent System and the Single-Agent System.

## Overview

The travel agent systems are designed to handle various travel-related queries, including:
- Flight and hotel bookings
- Destination recommendations
- General travel information
- Travel tips and local attractions

## Multi-Agent System (`TravelAgentSystem`)

The multi-agent system uses a specialized agent approach, where different agents handle specific types of queries.

### Architecture

The system consists of three specialized agents:

1. **Booking Agent**
   - Handles flight and hotel bookings
   - System prompt focused on booking-related tasks
   - Tools: `_search_flights`, `_search_hotels`, `_book_flight`, `_book_hotel`, `_get_booking_status`

2. **Recommendation Agent**
   - Provides destination recommendations
   - System prompt focused on suggesting destinations
   - Tools: `_search_destinations`, `_get_destination_recommendations`, `_get_travel_tips`, `_get_local_attractions`

3. **General Agent**
   - Handles general travel-related queries
   - System prompt focused on providing general travel information
   - Tools: `_search_travel_info`

### Query Processing Flow

1. User submits a query
2. System determines query type based on keywords:
   - Booking queries: "book", "reserve", "schedule"
   - Recommendation queries: "recommend", "suggest", "where should"
   - General queries: all other queries
3. Query is routed to appropriate specialized agent
4. Agent processes query using relevant tools
5. Response is returned to user

### Key Features

- Specialized agents for different query types
- Separate message histories for each agent
- Token usage tracking
- Integration with external data sources
- Traceable operations for monitoring and debugging

## Single-Agent System (`SingleTravelAgent`)

The single-agent system uses a unified approach, where one agent handles all types of queries.

### Architecture

The system consists of a single comprehensive agent that can handle all types of travel-related queries.

### Query Processing Flow

1. User submits a query
2. Single agent processes the query
3. Agent determines appropriate tools to use
4. Response is returned to user

### Key Features

- Unified agent for all query types
- Single message history
- Token usage tracking
- Integration with external data sources
- Traceable operations for monitoring and debugging

## Comparison

### Multi-Agent System Advantages
- Specialized agents for specific tasks
- Potentially better performance for complex queries
- Clear separation of concerns
- Easier to maintain and update individual components

### Single-Agent System Advantages
- Simpler architecture
- Easier to implement
- No need for query routing
- Single point of maintenance

## Tools and Capabilities

Both systems provide the following core tools:

1. **Flight Operations**
   - Search flights
   - Book flights
   - Get flight booking status

2. **Hotel Operations**
   - Search hotels
   - Book hotels
   - Get hotel booking status

3. **Destination Services**
   - Search destinations
   - Get destination recommendations
   - Get travel tips
   - Get local attractions

4. **General Information**
   - Search travel information

## Implementation Details

### Dependencies
- OpenAI GPT-4 model
- Pydantic for data validation
- LangSmith for tracing
- Custom data sources for flights, hotels, and destinations

### Data Models
- `TravelQuery`: Base query model
- `TravelResponse`: Response model
- `FlightDetails`: Flight information
- `HotelDetails`: Hotel information
- `DestinationRecommendation`: Destination recommendations

### Error Handling
Both systems include error handling for:
- Failed queries
- Invalid inputs
- External service failures
- Token usage limits

## Usage Examples

### Multi-Agent System
```python
system = TravelAgentSystem(knowledge_base)
response = await system.process_query("Book a flight from New York to London")
```

### Single-Agent System
```python
agent = SingleTravelAgent()
response = await agent.process_query("Book a flight from New York to London")
```

## Best Practices

1. **Query Formulation**
   - Be specific in queries
   - Include relevant dates and locations
   - Specify preferences clearly

2. **System Selection**
   - Use multi-agent system for complex, specialized queries
   - Use single-agent system for simpler, general queries

3. **Error Handling**
   - Implement proper error handling
   - Provide meaningful error messages
   - Log errors for debugging

4. **Performance Optimization**
   - Monitor token usage
   - Cache frequently accessed data
   - Optimize tool usage 