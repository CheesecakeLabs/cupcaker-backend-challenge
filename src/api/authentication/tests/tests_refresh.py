import json
from typing import Callable

import jwt
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from rest_framework import status

from api.authentication.helpers.settings import api_settings


def test_use_refresh_token_generate_tokens_with_full_user_data(
    make_user: Callable, make_refresh_token: Callable, client: Client
) -> None:
    """Check if refresh endpoint successfully refreshes a token"""
    user = make_user()
    refresh_token = make_refresh_token(user)

    response = client.post(
        path=reverse("auth:token-refresh"),
        data=json.dumps({"refresh": str(refresh_token)}),
        content_type="application/json",
    )

    response_data = response.json()
    new_access_token = response_data.get("access")
    new_refresh_token = response_data.get("refresh")

    assert response.status_code == status.HTTP_200_OK
    assert new_access_token
    assert new_refresh_token

    new_access_token_data = jwt.decode(
        str(new_access_token),
        settings.SIMPLE_JWT.get("SIGNING_KEY"),
        api_settings.ALGORITHM,
    )

    new_refresh_token_data = jwt.decode(
        str(new_refresh_token),
        settings.SIMPLE_JWT.get("SIGNING_KEY"),
        api_settings.ALGORITHM,
    )

    access_token_user = new_access_token_data.get("user")
    refresh_token_user = new_refresh_token_data.get("user")

    user_data = {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
    }

    assert access_token_user == user_data
    assert refresh_token_user == user_data
