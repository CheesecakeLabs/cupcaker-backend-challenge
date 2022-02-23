import json
from typing import Callable

from django.test.client import Client
from django.urls import reverse
from pytest_mock.plugin import MockerFixture
from rest_framework import status
from rest_framework.response import Response

from api.authentication import messages

PASSWORD = "123456"


def signin(client: Client, email: str, password: str) -> Response:
    """
    Make a request to the signin endpoint
    Args:
        client: HTTP Client
        email: The email from the user that is trying to signin
        password: The password from the user that is trying to signin
    Returns: Signin endpoint response
    """

    return client.post(
        path=reverse("auth:signin"),
        data=json.dumps({"email": email, "password": password}),
        content_type="application/json",
    )


def test_signin_successfully(
    client: Client,
    make_user: Callable,
    make_refresh_token: Callable,
    mocker: MockerFixture,
) -> None:
    """Check if a user signin with correct email and password is succesful"""
    user = make_user()
    refresh_token = make_refresh_token(user)

    mocker.patch(
        "api.authentication.helpers.tokens.AccessToken",
        return_value=refresh_token.access_token,
    )
    mocker.patch(
        "api.authentication.helpers.tokens.RefreshToken.for_user",
        return_value=refresh_token,
    )

    response = signin(client=client, email=user.email, password=PASSWORD)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "access_token": str(refresh_token.access_token),
        "refresh_token": str(refresh_token),
    }


def test_signin_with_incorrect_format_email(client: Client) -> None:
    """Check if the user signin with incorrect email format response is consistent"""
    response = signin(client=client, email="incorrect.format.email", password=PASSWORD)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"email": ["Enter a valid email address."]}


def test_signin_with_incorrect_email(client: Client, make_user: Callable) -> None:
    """Check if the signin with an incorrect email gives a consistent error message"""
    make_user()

    response = signin(
        client=client, email="incorrect.email@example.com", password=PASSWORD
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": messages.WRONG_CREDENTIALS}


def test_singin_with_incorrect_password(client: Client, make_user: Callable) -> None:
    """Check if the signin with an incorrect password gives a consistent error message"""
    user = make_user()

    response = signin(client=client, email=user.email, password="incorrect_password")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": messages.WRONG_CREDENTIALS}


def test_singin_with_empty_fields(client: Client) -> None:
    """Check if the signin with empty fields gives a consistent error message"""
    response = signin(client=client, email="", password="")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "email": ["This field may not be blank."],
        "password": ["This field may not be blank."],
    }


def test_signin_with_trimmable_password_correctly(
    client: Client,
    db,
    make_user: Callable,
    make_refresh_token: Callable,
    mocker: MockerFixture,
) -> None:
    """Check if the signin with a trimmable password (starting or/and ending with a blank space) works correctly"""
    trimmable_password = f"{PASSWORD} "
    user = make_user(password=trimmable_password)
    refresh_token = make_refresh_token(user)

    mocker.patch(
        "api.authentication.helpers.tokens.AccessToken",
        return_value=refresh_token.access_token,
    )
    mocker.patch(
        "api.authentication.helpers.tokens.RefreshToken.for_user",
        return_value=refresh_token,
    )

    response = signin(client=client, email=user.email, password=trimmable_password)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "access_token": str(refresh_token.access_token),
        "refresh_token": str(refresh_token),
    }


def test_signin_into_an_account_with_trimmable_password_trimming_it_unsuccessfully(
    client: Client, db, make_user: MockerFixture
) -> None:
    """
    Check if a user cannot signin on an account that has a trimmable password
    (starting or/and ending with a blank space) when passing the trimmed string to the endpoint
    """
    user = make_user(password=f" {PASSWORD}")

    response = signin(client=client, email=user.email, password=PASSWORD)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": messages.WRONG_CREDENTIALS}
