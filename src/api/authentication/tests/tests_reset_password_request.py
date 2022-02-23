import json
from typing import Any, Callable

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from django.test.client import Client
from django.urls import reverse
from pytest_mock.plugin import MockerFixture
from rest_framework import status
from rest_framework.response import Response

from api.authentication import messages
from api.authentication.models import Code

User = get_user_model()


def reset_password_code_request(client: Client, email: str) -> Response:
    """
    Make a request to the reset password code request endpoint
    Args:
        client: HTTP Client
        email: User email from which the request code will be sent
    Returns: Reset password request code endpoint response
    """
    return client.post(
        path=reverse("auth:reset-password-request-code"),
        data=json.dumps({"email": email}),
        content_type="application/json",
    )


@override_settings(DEFAULT_MESSENGER="EMAIL")
def test_successful_reset_password_email_code_request(
    client: Client, user_1: User
) -> None:
    """Check if the `reset-password code request` endpoint sends the reset-password email with the valid code"""
    response = reset_password_code_request(client=client, email=user_1.email)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == messages.SUCCESS

    reset_password_requests = Code.objects.all()
    assert len(reset_password_requests) == 1

    reset_password_request = reset_password_requests[0]

    assert reset_password_request.user == user_1
    assert reset_password_request.was_used is False
    assert reset_password_request.code is not None

    assert len(mail.outbox) == 1
    assert reset_password_request.code in mail.outbox[0].body
    assert reset_password_request.user.email in mail.outbox[0].recipients()


@override_settings(DEFAULT_MESSENGER="SMS")
def test_successful_reset_password_sms_code_request(
    client: Client, user_1: User, mocker: MockerFixture
) -> None:
    """Check if the `reset-password code request` endpoint sends the reset-password SMS with the valid code"""

    class MockedBoto3:
        def __init__(*args: Any, **kwargs: Any) -> None:
            return

        def publish(*args: Any, **kwargs: Any) -> None:
            return

    spy = mocker.spy(MockedBoto3, "publish")

    mocked_number = "555"
    mocker.patch("api.core.messenger.sms.boto3.client", new=MockedBoto3)
    mocker.patch("api.core.messenger.sms.SMS.get_recipient", return_value=mocked_number)
    response = reset_password_code_request(client=client, email=user_1.email)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == messages.SUCCESS

    reset_password_requests = Code.objects.all()
    assert len(reset_password_requests) == 1

    reset_password_request = reset_password_requests[0]
    assert reset_password_request.user == user_1
    assert reset_password_request.was_used is False
    assert reset_password_request.code is not None
    assert spy.call_count == 1
    kwargs = spy.call_args.kwargs
    assert kwargs["PhoneNumber"] == mocked_number
    assert reset_password_request.code in kwargs["Message"]


def test_invalid_user_reset_password_code_request(
    client: Client, make_user: Callable
) -> None:
    """Check if the `reset-password code request` endpoint gives an consistent message for a request with an invalid email"""
    make_user()
    response = reset_password_code_request(client=client, email="invalid@ckl.io")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == messages.USER_NOT_FOUND

    assert Code.objects.count() == 0
