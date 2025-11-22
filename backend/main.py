"""
Inkle Tourism API - Main FastAPI application.

A multi-agent system for providing tourism information including:
- Location validation and geocoding
- Real-time weather data
- Tourist attraction recommendations

All data is fetched from real APIs (Open-Meteo, Overpass, Nominatim).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .orchestrator.tourism_orchestrator import TourismOrchestrator

app = FastAPI(
    title="Inkle Tourism API",
    description="Multi-agent tourism information system",
    version="1.0.0",
)

# CORS so the Netlify frontend can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://deft-conkies-526391.netlify.app",  # your frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    """Request model for tourism queries."""
    query: str = Field(
        ...,
        description="Natural language query about a tourism destination",
        min_length=1,
        example="What's the weather like in Paris?",
    )


class QueryResponse(BaseModel):
    """Response model for tourism queries."""
    response: str = Field(
        ...,
        description="Formatted response with tourism information",
    )


@app.get("/")
async def root() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        A welcome message indicating the API is running
    """
    return {"message": "Inkle Tourism API is running"}


@app.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest) -> QueryResponse:
    """
    Process a tourism query through the multi-agent orchestrator.

    Args:
        request: QueryRequest containing the user's natural language query

    Returns:
        QueryResponse with formatted tourism information including:
        - Weather conditions (temperature, precipitation probability)
        - Tourist attractions (up to 5 places)
        - Error message if location doesn't exist
    """
    result = TourismOrchestrator.handle_query(request.query)
    return QueryResponse(response=result)

