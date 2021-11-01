import requests
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.conf.settings import FIREBASE_APP_API_KEY

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    base_path = "https://identitytoolkit.googleapis.com"
    payload = {
        "email": form_data.username,
        "password": form_data.password,
        'returnSecureToken': True
    }
    # Post request
    r = requests.post(
        f"{base_path}/v1/accounts:signInWithPassword?key={FIREBASE_APP_API_KEY}",
        data=payload
    )
    keys = r.json().keys()
    # Check for errors
    if "error" in keys:
        error = r.json()["error"]
        raise HTTPException(
            status_code=error["code"],
            headers={"WWW-Authenticate": "Bearer"},
            detail=dict(
                code=f"{error['code']}004",
                title="NotAuthorized",
                message=error["message"]
            )
        )
    # success
    auth = r.json()
    auth["token_type"] = "bearer"
    auth["access_token"] = auth.pop("idToken")
    return auth
