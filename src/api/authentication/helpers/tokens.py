from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework_simplejwt import authentication, tokens
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken

from .settings import api_settings

User = get_user_model()


class JWTAuthentication(authentication.JWTAuthentication):
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_CLAIM][
                api_settings.USER_ID_FIELD
            ]
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")

        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")

        return user


class JWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = JWTAuthentication
    name = "JWT"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
        }


class Token(tokens.Token):
    @classmethod
    def for_user(cls, user: User) -> tokens.Token:
        """
        Returns an authorization token for the given user that will be provided
        after authenticating the user's credentials.
        """
        user_dict = user.__dict__
        token = cls()
        token[api_settings.USER_CLAIM] = {
            key: str(user_dict[key])
            for key in user_dict.keys()
            if key in api_settings.USER_CLAIM_FIELDS
        }

        return token


class RefreshToken(tokens.RefreshToken, Token):
    @property
    def access_token(self):
        """
        Returns an access token created from this refresh token.  Copies all
        claims present in this refresh token to the new access token except
        those claims listed in the `no_copy_claims` attribute.
        """
        access = AccessToken()

        # Use instantiation time of refresh token as relative timestamp for
        # access token "exp" claim.  This ensures that both a refresh and
        # access token expire relative to the same time if they are created as
        # a pair.
        access.set_exp(from_time=self.current_time)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value

        return access


class AccessToken(tokens.AccessToken, Token):
    pass


def get_tokens_for_user(user: User) -> dict:
    """
    Get access and refresh tokens for the user
    Params:
        user: The user from which the tokens are going to be retrieved
    Returns: The user's access and refresh tokens
    """
    refresh_token = RefreshToken.for_user(user)
    return {
        "access_token": str(refresh_token.access_token),
        "refresh_token": str(refresh_token),
    }


def refresh_token(token: str) -> dict:
    """
    Refresh the tokens
    Params:
        token: The refresh token that will generate the new tokens
    Returns: The new access and refresh tokens
    """
    refresh = RefreshToken(token)

    result = {"access": str(refresh.access_token)}
    if api_settings.ROTATE_REFRESH_TOKENS:
        if api_settings.BLACKLIST_AFTER_ROTATION:
            try:
                # Attempt to blacklist the given refresh token
                refresh.blacklist()
            except AttributeError:
                # If blacklist app not installed, `blacklist` method will
                # not be present
                pass

        refresh.set_jti()
        refresh.set_exp()
        result["refresh"] = str(refresh)

    return result
