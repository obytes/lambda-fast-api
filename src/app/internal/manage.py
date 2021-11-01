from fastapi import APIRouter

router = APIRouter(
    prefix="/manage",
    tags=["manage"],
)


@router.get("/hc")
async def health_check():
    return {"status": "I'm sexy and I know It!"}
