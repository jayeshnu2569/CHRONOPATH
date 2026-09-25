from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.decision import router as decision_router


app = FastAPI(
    title="ChronoPath AI API",
    description="AI-assisted Future Decision Simulation and Decision Support System",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(decision_router)


@app.get("/")
def root():
    return {
        "project": "ChronoPath AI",
        "status": "running",
        "message": "ChronoPath AI backend is operational"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }