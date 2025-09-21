# Minimal Vercel handler that works
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create minimal FastAPI app
app = FastAPI(
    title="iZonehub API",
    version="1.0.0",
    description="API for iZonehub Makerspace"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to iZonehub API", 
        "status": "running",
        "environment": "vercel",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/test")
async def test():
    return {"message": "API is working on Vercel!"}

# Basic auth endpoint for testing
@app.post("/api/auth/test")
async def test_auth():
    return {"message": "Auth endpoint working"}

# Export for Vercel
handler = app