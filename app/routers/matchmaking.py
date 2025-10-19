import logging

from fastapi import APIRouter

from app.models.request.simple_matchmaking_input import (
    SimpleMatchmakingInput,
    SquadMatchmakingInput,
)
from app.models.response.simple_matchmaking_output import (
    SimpleMatchmakingOutput,
    SquadMatchmakingOutput,
)
from app.services.matchmaking.simple import SimpleMatchmakingService
from app.services.matchmaking.squad import SquadMatchmakingService
from app.storage.players_db import players_db, squad_players_db

router = APIRouter(prefix="/matches", tags=["matchmaking"])
logger = logging.getLogger(__name__)


@router.post("/simple", response_model=SimpleMatchmakingOutput)
async def match_simple(request: SimpleMatchmakingInput) -> SimpleMatchmakingOutput:
    matches = SimpleMatchmakingService(players_db).do_matchmaking(new_players=request.players)

    # Log resulting matches and average balance performance
    if matches:
        avg_disbalance = sum(match.calc_disbalance() for match in matches) / len(matches)
        logger.info(f"Simple matchmaking: {len(matches)} matches created, avg disbalance: {avg_disbalance:.1f}")
    else:
        logger.info("Simple matchmaking: no matches created")

    return SimpleMatchmakingOutput(matches=matches)


@router.post("/squad", response_model=SquadMatchmakingOutput)
async def match_squad(request: SquadMatchmakingInput) -> SquadMatchmakingOutput:
    matches = SquadMatchmakingService(squad_players_db).do_matchmaking(new_players=request.players)

    # Log resulting matches and average balance performance
    if matches:
        avg_disbalance = sum(match.calc_disbalance() for match in matches) / len(matches)
        logger.info(f"Squad matchmaking: {len(matches)} matches created, avg disbalance: {avg_disbalance:.1f}")
    else:
        logger.info("Squad matchmaking: no matches created")

    return SquadMatchmakingOutput(matches=matches)
