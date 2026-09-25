from fastapi import APIRouter, HTTPException

from models.decision import DecisionRequest
from services.decision_engine import calculate_scores


router = APIRouter(
    prefix="/api/decision",
    tags=["Decision Engine"]
)


@router.post("/analyze")
def analyze_decision(request: DecisionRequest):

    try:

        results = calculate_scores(
            request.criteria,
            request.option_scores
        )

        return {
            "decision": request.title,
            "results": results
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )