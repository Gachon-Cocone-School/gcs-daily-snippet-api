from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from contextlib import asynccontextmanager
from app.api.api import api_router

# Define lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown: cleanup if needed
    # No cleanup needed for now

# Create FastAPI app with lifespan
app = FastAPI(
    title="Daily Snippets API",
    description="API for retrieving daily snippets based on filters",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router)

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 4001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)