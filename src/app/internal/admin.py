from fastapi import APIRouter, Request, Depends

from app.dependencies.auth import RBAC

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.get(
    "/endpoints",
    dependencies=[Depends(RBAC(allowed_groups=["ADMINS"]))]
)
async def list_endpoints(request: Request):
    endpoints = [
        {'path': route.path, 'name': route.name}
        for route in request.app.routes
    ]
    return endpoints
