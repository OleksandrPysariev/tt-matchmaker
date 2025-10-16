from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["root"])


@router.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")
