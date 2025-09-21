from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from iZonehub API on Vercel!", "status": "working"}

@app.get("/health")
def health():
    return {"status": "healthy", "platform": "vercel"}

@app.get("/api/test")
def test():
    return {"message": "API endpoint working!", "success": True}

# Wrap FastAPI app with Mangum for serverless
handler = Mangum(app)