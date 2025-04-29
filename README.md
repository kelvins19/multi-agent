# Travel Agent System

This project implements a multi-agent travel assistant using Pydantic AI for agent delegation and ChromaDB for knowledge storage.

## Project Structure

```
.
├── src/
│   ├── agents/         # Agent definitions and configurations
│   ├── models/         # Pydantic models for data validation
│   ├── retrievers/     # Knowledge retrieval components
│   ├── utils/          # Utility functions
│   └── config.py       # Configuration management
├── tests/              # Test files
├── data/               # Data storage
├── .env.example        # Environment variables template
└── requirements.txt    # Project dependencies
```

## Features

- Multi-agent travel assistant with specialized agents:
  - Booking Agent: Handles flight and hotel bookings
  - Recommendation Agent: Suggests travel destinations
  - General Inquiry Agent: Answers general travel questions
- Agent delegation pattern for complex workflows
- Knowledge storage with ChromaDB
- Document processing utilities
- Type-safe data handling with Pydantic models

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```
5. Run the application:
   ```bash
   python src/main.py
   ```

## How It Works

The system uses a multi-agent approach with Pydantic AI:

1. **Booking Agent**: Handles flight and hotel bookings
2. **Recommendation Agent**: Suggests travel destinations based on user preferences
3. **General Inquiry Agent**: Answers general travel questions using the knowledge base

Each agent is specialized for a specific task and communicates through a shared knowledge base, which uses ChromaDB to store and retrieve information.

## Example Usage

```python
import asyncio
from src.agents.travel_agent import TravelAgentSystem
from src.models.base import TravelQuery

async def main():
    # Initialize the travel agent system
    travel_system = TravelAgentSystem()
    
    # Process a booking query
    booking_query = TravelQuery(
        text="I need to book a flight from New York to Paris on June 15, 2023",
        query_type="booking"
    )
    booking_response = await travel_system.process_query(booking_query)
    print(f"Answer: {booking_response.answer}")
    
    # Process a recommendation query
    recommendation_query = TravelQuery(
        text="I'm looking for a beach destination with good food and culture",
        query_type="recommendation"
    )
    recommendation_response = await travel_system.process_query(recommendation_query)
    print(f"Answer: {recommendation_response.answer}")
    
    # Process a general query
    general_query = TravelQuery(
        text="What's the best time to visit Europe?",
        query_type="general"
    )
    general_response = await travel_system.process_query(general_query)
    print(f"Answer: {general_response.answer}")

if __name__ == "__main__":
    asyncio.run(main())
```

## License

MIT 