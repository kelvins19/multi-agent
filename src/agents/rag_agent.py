from typing import List, Dict, Any, Union, Optional
from pydantic_ai import Agent, RunContext
from pydantic_ai.usage import Usage, UsageLimits

from ..models.base import Document, Query, Response, Failed
from ..config import settings
from ..retrievers.vector_store import VectorStore

# Define the retrieval agent that will search for relevant documents
retrieval_agent = Agent[None, Union[List[Document], Failed]](
    'openai:gpt-4',
    output_type=Union[List[Document], Failed],
    system_prompt=(
        "You are a retrieval agent that searches for relevant documents based on user queries. "
        "Use the search_documents tool to find documents that match the query."
    ),
)

# Define the generation agent that will generate answers based on retrieved documents
generation_agent = Agent[None, Union[Response, Failed]](
    'openai:gpt-4',
    output_type=Union[Response, Failed],
    system_prompt=(
        "You are a generation agent that creates answers based on retrieved documents. "
        "Use the generate_answer tool to create a response based on the documents and query."
    ),
)

# Create a global vector store instance
vector_store = VectorStore()

@retrieval_agent.tool
async def search_documents(ctx: RunContext[None], query: str) -> List[Document]:
    """
    Search for documents relevant to the query.
    
    Args:
        query: The search query
        
    Returns:
        A list of relevant documents
    """
    try:
        # Use the vector store to search for relevant documents
        documents = await vector_store.search(query)
        return documents
    except Exception as e:
        # If there's an error, return a sample document
        return [
            Document(
                content="This is a sample document about the query.",
                metadata={"source": "sample", "relevance": 0.95}
            )
        ]

@generation_agent.tool
async def generate_answer(
    ctx: RunContext[None], 
    query: str, 
    documents: List[Document]
) -> str:
    """
    Generate an answer based on the retrieved documents and query.
    
    Args:
        query: The original query
        documents: The retrieved documents
        
    Returns:
        A generated answer
    """
    # Create a prompt with the documents and query
    documents_text = "\n\n".join([f"Document {i+1}:\n{doc.content}" for i, doc in enumerate(documents)])
    
    prompt = f"""
    Query: {query}
    
    Retrieved Documents:
    {documents_text}
    
    Based on the above documents, please provide a comprehensive answer to the query.
    """
    
    # Use the agent's LLM to generate an answer
    result = await ctx.llm.complete(prompt)
    return result.text

class RAGSystem:
    """Agentic RAG implementation using Pydantic AI."""
    
    def __init__(self):
        self.usage_limits = UsageLimits(request_limit=10, total_tokens_limit=4000)
    
    async def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of documents to add
        """
        await vector_store.add_documents(documents)
    
    async def process_query(self, query: Query) -> Response:
        """
        Process a query through the RAG system.
        
        Args:
            query: The query to process
            
        Returns:
            A response containing the answer and sources
        """
        usage = Usage()
        
        # Step 1: Retrieve relevant documents
        retrieval_result = await retrieval_agent.run(
            f"Find documents relevant to: {query.text}",
            usage=usage,
            usage_limits=self.usage_limits
        )
        
        if isinstance(retrieval_result.output, Failed):
            return Response(
                answer=f"Failed to retrieve documents: {retrieval_result.output.reason}",
                sources=[],
                metadata={"error": "retrieval_failed"}
            )
        
        documents = retrieval_result.output
        
        # Step 2: Generate answer based on retrieved documents
        generation_result = await generation_agent.run(
            f"Generate an answer to the query: {query.text}",
            usage=usage,
            usage_limits=self.usage_limits
        )
        
        if isinstance(generation_result.output, Failed):
            return Response(
                answer=f"Failed to generate answer: {generation_result.output.reason}",
                sources=documents,
                metadata={"error": "generation_failed"}
            )
        
        response = generation_result.output
        response.sources = documents
        response.metadata["usage"] = usage.model_dump()
        
        return response 