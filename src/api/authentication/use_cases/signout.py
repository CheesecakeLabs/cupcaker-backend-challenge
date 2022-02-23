from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError

from api.authentication import messages
from api.authentication.helpers.tokens import RefreshToken
from api.core.use_cases.base import BaseUseCase

User = get_user_model()


class SignoutUseCase(BaseUseCase):
    def execute(self, refresh_token: str) -> None:
        """
        Blocklist the refresh_tokenj
        Params:
            refresh_token: The token that'll be blocklisted
        """
        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            raise AuthenticationFailed(detail=messages.INVALID_ACCESS_TOKEN)
