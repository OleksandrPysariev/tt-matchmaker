from fastapi import APIRouter

from app.models.request.simple_matchmaking_input import SimpleMatchmakingInput
from app.models.response.simple_matchmaking_output import SimpleMatchmakingOutput
from app.services.matchmaking.simple import SimpleMatchmakingService

router = APIRouter(prefix="/matches", tags=["matchmaking"])

@router.post("/simple")
async def match_simple(request: SimpleMatchmakingInput) -> SimpleMatchmakingOutput:
    match = SimpleMatchmakingService().do_matchmaking(request.players)
    return SimpleMatchmakingOutputResponseBuilder.build(match)
