from typing import List, Optional, Dict

from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from app.conf import settings


class RBAC(OAuth2PasswordBearer):
    def __init__(
            self,
            token_url: str = f"/{settings.AWS_API_GW_MAPPING_KEY}/v1/auth/token",
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            description: Optional[str] = None,
            auto_error: bool = True,
            allowed_groups: List = None
    ):
        super().__init__(
            tokenUrl=token_url,
            scheme_name=scheme_name,
            scopes=scopes,
            description=description,
            auto_error=auto_error,
        )
        self.allowed_groups = allowed_groups

    async def __call__(self, request: Request):
        await self.get_claims(request)

        if self.allowed_groups:
            if not request.state.groups:
                raise HTTPException(
                    status_code=401,
                    headers={"WWW-Authenticate": "Bearer"},
                    detail=dict(
                        code="401002",
                        title="NotAuthorized",
                        message="The endpoint has authorization check and the caller does not belong to any groups"
                    )
                )
            else:
                if not any(group in self.allowed_groups for group in request.state.groups):
                    raise HTTPException(
                        status_code=401,
                        headers={"WWW-Authenticate": "Bearer"},
                        detail=dict(
                            code="401003",
                            title="NotAuthorized",
                            message=f'Only {self.allowed_groups} can access this endpoint'
                        )
                    )

    @staticmethod
    async def get_claims(request: Request):
        request.state.access_token = request.headers.get('Authorization').split()[1]
        claims = request.scope["aws.event"]["requestContext"]["authorizer"]["jwt"]["claims"]
        request.state.claims = claims
        request.state.username = claims["sub"]
        request.state.groups = claims.get(settings.JWT_AUTHORIZATION_GROUPS_ATTR_NAME, "[]").strip("[]").split()
