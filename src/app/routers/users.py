from fastapi import APIRouter, Depends, Request

from app.dependencies.auth import RBAC

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/whoami",
    dependencies=[Depends(RBAC(allowed_groups=["USERS", "ADMINS"]))]
)
async def whoami(request: Request):
    return {"claims": request.state.claims}
