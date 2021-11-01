import os

from fastapi import FastAPI

from app.conf.settings import AWS_API_GW_MAPPING_KEY
from app.internal import manage, admin
from app.routers import users, auth

v1 = FastAPI(
    title="Lambda Fast API Starter",
    description="Fast API Starter, Deployed on AWS Lambda and served with AWS API Gateway",
    version="0.1.0",
    # In case api gateway is configured with custom domain
    root_path=os.path.join(f"/{AWS_API_GW_MAPPING_KEY}", "v1")
)


def register_routers(app: FastAPI):
    app.mount(f"/v1", v1)
    # Register routers
    v1.include_router(manage.router)
    v1.include_router(admin.router)
    v1.include_router(auth.router)
    v1.include_router(users.router)
