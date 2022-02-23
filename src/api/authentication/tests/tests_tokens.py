from typing import Callable

import jwt
from django.conf import settings

from api.authentication.helpers.settings import api_settings
from api.authentication.helpers.tokens import AccessToken, RefreshToken


def test_generated_refresh_token_contains_all_user_information(
    make_user: Callable,
) -> None:
    """Check if the refreshened token has the user's information"""
    user = make_user()

    refresh_token = RefreshToken.for_user(user)
    token_data = jwt.decode(
        str(refresh_token),
        settings.SIMPLE_JWT.get("SIGNING_KEY"),
        api_settings.ALGORITHM,
    )
    user_data = token_data.get("user")

    assert token_data.get("token_type") == "refresh"
    assert user_data
    assert user_data == {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
    }


def test_generated_refresh_tokens_access_token_contains_all_user_information(
    make_user: Callable,
) -> None:
    """Check if a refreshened access token has the user's information"""
    user = make_user()

    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token
    token_data = jwt.decode(
        str(access_token),
        settings.SIMPLE_JWT.get("SIGNING_KEY"),
        api_settings.ALGORITHM,
    )
    user_data = token_data.get("user")

    assert token_data.get("token_type") == "access"
    assert user_data
    assert user_data == {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
    }


def test_generated_access_token_contains_all_user_information(
    make_user: Callable,
) -> None:
    """Check if a generated access token has the user's information"""
    user = make_user()

    access_token = AccessToken.for_user(user)
    token_data = jwt.decode(
        str(access_token),
        settings.SIMPLE_JWT.get("SIGNING_KEY"),
        api_settings.ALGORITHM,
    )
    user_data = token_data.get("user")

    assert token_data.get("token_type") == "access"
    assert user_data
    assert user_data == {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
    }
