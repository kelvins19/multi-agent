from typing import List, Dict, Any, Callable, Optional
from src.models.base import TravelQuery, TravelResponse

class BaseAgent:
    """Base class for all specialized agents in the travel system."""
    
    def __init__(
        self,
        name: str,
        system_prompt: str,
        tools: List[Callable]
    ):
        """
        Initialize a base agent.
        
        Args:
            name: The name of the agent
            system_prompt: The system prompt that defines the agent's role
            tools: List of tools (functions) available to the agent
        """
        self.name = name
        self.system_prompt = system_prompt
        self.tools = tools
    
    async def process_query(self, query: TravelQuery) -> TravelResponse:
        """
        Process a travel query and return a response.
        
        Args:
            query: The travel query to process
            
        Returns:
            A travel response containing the answer and metadata
        """
        # This is a base implementation that should be overridden by specialized agents
        return TravelResponse(
            answer="I'm sorry, I'm not sure how to help with that specific request. Please try rephrasing your question or ask for something else.",
            sources=[],
            metadata={"agent": self.name}
        )
    
    def _validate_tool(self, tool_name: str) -> Optional[Callable]:
        """
        Validate and return a tool by name.
        
        Args:
            tool_name: The name of the tool to validate
            
        Returns:
            The tool function if found, None otherwise
        """
        for tool in self.tools:
            if tool.__name__ == tool_name:
                return tool
        return None 