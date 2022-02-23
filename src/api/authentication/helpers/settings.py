from rest_framework.settings import DEFAULTS
from rest_framework_simplejwt import settings as jwt_settings

DEFAULTS = {
    **jwt_settings.DEFAULTS,
    "USER_ID_FIELD": "id",
    "USER_CLAIM": "user",
    "USER_CLAIM_FIELDS": ["id", "email", "full_name"],
}

api_settings = jwt_settings.APISettings(
    jwt_settings.USER_SETTINGS, DEFAULTS, jwt_settings.IMPORT_STRINGS
)
