import json
from typing import Tuple

from django.contrib.auth import authenticate, get_user_model
from django.test.client import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from api.authentication import messages

User = get_user_model()


def reset_password(client: Client, uidb64: str, token: str, password: str) -> Response:

    """
    Make a request to the reset password endpoint
    Args:
        client: HTTP Client
        uidb64: User's encrypted primary key
        token: Expirable token that authenticates the user
        password: New password
    Returns: Reset password validate code endpoint response
    """
    return client.post(
        path=reverse("auth:reset-password", kwargs={"uidb64": uidb64, "token": token}),
        data=json.dumps({"password": password}),
        content_type="application/json",
    )


def test_successful_reset_password(
    client: Client, user_1: User, user_1_reset_password_data: Tuple[str, str]
) -> None:
    """Check if a user with valid request data can reset its password"""
    uidb64, token = user_1_reset_password_data
    new_password = "Valid Password"
    response = reset_password(
        client=client, uidb64=uidb64, token=token, password=new_password
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == messages.SUCCESS
    user = authenticate(email=user_1.email, password=new_password)
    assert user.id == user_1.id


def test_invalid_uidb64_reset_password(
    client: Client, user_1: User, user_1_reset_password_data: Tuple[str, str]
) -> None:
    """Check if a reset password attempt with an invalid uidb64 returns a consistent error message"""
    _, token = user_1_reset_password_data
    invalid_uidb64 = "LTE"
    new_password = "Valid Password"
    response = reset_password(
        client=client, uidb64=invalid_uidb64, token=token, password=new_password
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    user = authenticate(email=user_1.email, password=new_password)
    assert user is None


def test_invalid_token_reset_password(
    client: Client, user_1: User, user_1_reset_password_data: Tuple[str, str]
) -> None:
    """Check if a reset password attempt with an invalid token returns a consistent error message"""
    uidb64, _ = user_1_reset_password_data
    invalid_token = "wrong"
    new_password = "Valid Password"
    response = reset_password(
        client=client, uidb64=uidb64, token=invalid_token, password=new_password
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    user = authenticate(email=user_1.email, password=new_password)
    assert user is None


def test_successful_reset_password_with_a_trimmable_new_password(
    client: Client, user_1: User, user_1_reset_password_data: Tuple[str, str]
) -> None:
    """
    Check if when a user reset its password using a trimmable new password
    (starting or/and ending with a blank space) it is correctly stored in the database
    """
    uidb64, token = user_1_reset_password_data
    new_password = "Valid Trimmable Password "
    response = reset_password(
        client=client, uidb64=uidb64, token=token, password=new_password
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == messages.SUCCESS
    user = authenticate(email=user_1.email, password=new_password)
    assert user
    assert user.id == user_1.id
