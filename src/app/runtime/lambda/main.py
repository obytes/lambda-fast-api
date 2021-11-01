from fastapi import FastAPI
from mangum import Mangum

from app.api import register_routers
from app.conf import settings

app = FastAPI(
    title="Starter API",
    description="Starter Flask API Compatible with AWS API Gateway",
    version="0.1.0"
)

register_routers(app)
handler = Mangum(
    app,
    api_gateway_base_path=f"/{settings.AWS_API_GW_STAGE_NAME}"
)

# app.url_map.strict_slashes = False
# app.config["RESTX_JSON"] = {"indent": 4}
