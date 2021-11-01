import os


def get_list(env_name):
    return [x for x in os.environ.get(env_name, "").split(",") if x]


def get_bool(env_name, default="false"):
    return os.environ.get(env_name, default).lower() == "true"


# General
RUNTIME = os.environ.get("RUNTIME")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

# API
AWS_API_GW_STAGE_NAME = os.environ.get("AWS_API_GW_STAGE_NAME")
AWS_API_GW_MAPPING_KEY = os.environ.get("AWS_API_GW_MAPPING_KEY", default="fast")

# Firebase
FIREBASE_APP_API_KEY = os.environ.get("FIREBASE_APP_API_KEY")

# Authentication/Authorization
JWT_ISSUER_JWKS_URI = os.environ.get("JWT_ISSUER_JWKS_URI")
JWT_AUTHORIZED_AUDIENCES = os.environ.get("JWT_AUTHORIZED_AUDIENCES", "")
JWT_VERIFY_TOKEN_EXPIRATION = os.environ.get("JWT_VERIFY_TOKEN_EXPIRATION") == "true"
JWT_AUTHORIZATION_GROUPS_ATTR_NAME = os.environ["JWT_AUTHORIZATION_GROUPS_ATTR_NAME"]

