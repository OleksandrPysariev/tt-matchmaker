import logging

from fastapi import APIRouter

from app.models.request.simple_matchmaking_input import (
    SimpleMatchmakingInput,
    SquadMatchmakingInput,
    WaitlistSquadMatchmakingInput,
)
from app.models.response.simple_matchmaking_output import (
    SimpleMatchmakingOutput,
    SquadMatchmakingOutput,
    WaitlistSquadMatchmakingOutput,
)
from app.services.matchmaking.simple import SimpleMatchmakingService
from app.services.matchmaking.squad import SquadMatchmakingService
from app.services.matchmaking.waitlist_squad import WaitlistSquadMatchmakingService
from app.storage.players_db import players_db, squad_players_db, waitlist_squad_players_db

router = APIRouter(prefix="/matches", tags=["matchmaking"])
logger = logging.getLogger(__name__)


@router.post("/simple", response_model=SimpleMatchmakingOutput)
async def match_simple(request: SimpleMatchmakingInput) -> SimpleMatchmakingOutput:
    matches = SimpleMatchmakingService(players_db).do_matchmaking(new_players=request.players)

    if matches:
        avg_disbalance = sum(match.calc_disbalance() for match in matches) / len(matches)
        logger.info(f"Simple matchmaking: {len(matches)} matches created, avg disbalance: {avg_disbalance:.1f}")
    else:
        logger.info("Simple matchmaking: no matches created")

    return SimpleMatchmakingOutput(matches=matches)


@router.post("/squad", response_model=SquadMatchmakingOutput)
async def match_squad(request: SquadMatchmakingInput) -> SquadMatchmakingOutput:
    matches = SquadMatchmakingService(squad_players_db).do_matchmaking(new_players=request.players)

    if matches:
        avg_disbalance = sum(match.calc_disbalance() for match in matches) / len(matches)
        logger.info(f"Squad matchmaking: {len(matches)} matches created, avg disbalance: {avg_disbalance:.1f}")
    else:
        logger.info("Squad matchmaking: no matches created")

    return SquadMatchmakingOutput(matches=matches)


@router.post("/waitlist", response_model=WaitlistSquadMatchmakingOutput)
async def match_waitlist_squad(request: WaitlistSquadMatchmakingInput) -> WaitlistSquadMatchmakingOutput:
    matches = WaitlistSquadMatchmakingService(waitlist_squad_players_db).do_matchmaking(new_players=request.players)

    if matches:
        avg_disbalance = sum(match.calc_disbalance() for match in matches) / len(matches)
        logger.info(f"Squad matchmaking: {len(matches)} matches created, avg disbalance: {avg_disbalance:.1f}")
    else:
        logger.info("Squad matchmaking: no matches created")

    return WaitlistSquadMatchmakingOutput(matches=matches)
