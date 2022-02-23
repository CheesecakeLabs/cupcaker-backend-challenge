import json
from datetime import timedelta
from typing import Callable

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone
from api.authentication.models import Code
from pytest_mock.plugin import MockerFixture
from rest_framework import status
from rest_framework.response import Response

from api.authentication import messages

User = get_user_model()


def reset_password_request_code_validation(
    client: Client, email: str, code: str
) -> Response:
    """
    Make a request to the reset password code validation endpoint
    Args:
        client: HTTP Client
        email: User email from which the request code will validated
        code: The code that is being validated
    Returns: Reset password validate code endpoint response
    """
    return client.post(
        path=reverse("auth:reset-password-validate-code"),
        data=json.dumps(
            {
                "email": email,
                "code": code,
            }
        ),
        content_type="application/json",
    )


def test_successful_reset_password_code_validation(
    client: Client,
    user_1: User,
    make_reset_password_request: Callable,
    mocker: MockerFixture,
) -> None:
    """Check if reset password code validation returns valid user id and token"""
    reset_password_request = make_reset_password_request(
        user=user_1, type=Code.RESET_PASSWORD_REQUEST_TYPE
    )

    mocked_uidb64 = "uidb64"
    mocked_token = "token"

    mocker.patch(
        "api.authentication.use_cases.reset_password_validate_code.urlsafe_base64_encode",
        return_value=mocked_uidb64,
    )
    mocker.patch(
        "api.authentication.use_cases.reset_password_validate_code.default_token_generator.make_token",
        return_value=mocked_token,
    )

    response = reset_password_request_code_validation(
        client=client,
        email=reset_password_request.user.email,
        code=reset_password_request.code,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "token": mocked_token,
        "uidb64": mocked_uidb64,
    }
    reset_password_request.refresh_from_db()
    assert reset_password_request.was_used


def test_wrong_email_reset_password_code_validation(
    client: Client, user_1: User, make_reset_password_request: Callable
) -> None:
    """Check if the reset password code validation with wrong email has a consistent error message"""
    reset_password_request = make_reset_password_request(
        user=user_1, type=Code.RESET_PASSWORD_REQUEST_TYPE
    )

    response = reset_password_request_code_validation(
        client=client, email="invalid-email@ckl.io", code=reset_password_request.code
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == messages.RESET_PASSWORD_REQUEST_NOT_FOUND
    reset_password_request.refresh_from_db()
    assert reset_password_request.was_used is False


def test_wrong_code_reset_password_code_validation(
    client: Client, user_1: User, make_reset_password_request: Callable
) -> None:
    """Check if the reset password code validation with wrong code has a consistent error message"""
    reset_password_request = make_reset_password_request(
        user=user_1, type=Code.RESET_PASSWORD_REQUEST_TYPE
    )

    response = reset_password_request_code_validation(
        client=client, email=reset_password_request.user.email, code="invalid-code"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == messages.RESET_PASSWORD_REQUEST_NOT_FOUND
    reset_password_request.refresh_from_db()
    assert reset_password_request.was_used is False


@override_settings(FORGOT_TIME_EXPIRATION_TIME=timedelta(days=1))
def test_expired_reset_password_code_validation(
    client: Client, user_1: User, make_reset_password_request: Callable
):
    """Check if an expired reset password code validation has a consistent error message"""
    reset_password_request = make_reset_password_request(
        user=user_1, type=Code.RESET_PASSWORD_REQUEST_TYPE
    )
    reset_password_request.created = timezone.now() - timedelta(days=2)
    reset_password_request.save()

    response = reset_password_request_code_validation(
        client=client,
        email=reset_password_request.user.email,
        code=reset_password_request.code,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == messages.RESET_PASSWORD_SUBMIT_INVALID_CODE
    reset_password_request.refresh_from_db()
    assert reset_password_request.was_used is False


def test_reset_password_code_validation_twice(
    client: Client, user_1: User, make_reset_password_request: Callable
) -> None:
    """Check if the reset password code validation fails on the second attempt"""
    reset_password_request = make_reset_password_request(
        user=user_1, type=Code.RESET_PASSWORD_REQUEST_TYPE
    )

    reset_password_request_code_validation(
        client=client,
        email=reset_password_request.user.email,
        code=reset_password_request.code,
    )
    response = reset_password_request_code_validation(
        client=client,
        email=reset_password_request.user.email,
        code=reset_password_request.code,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == messages.RESET_PASSWORD_SUBMIT_INVALID_CODE
