from typing import Any, Callable, Tuple

import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from api.authentication.helpers.tokens import AccessToken, RefreshToken
from api.authentication.models import Code

User = get_user_model()


@pytest.fixture()
def make_user(db) -> Callable:
    def _make_user(
        email: str = "john.doe@example.com",
        password: str = "123456",
        full_name: str = "John Doe",
    ) -> User:
        user = User(
            email=email,
            password=make_password(password),
            full_name=full_name,
        )
        user.save()

        return user

    return _make_user


@pytest.fixture()
def make_refresh_token() -> Callable:
    def _make_refresh_token(user: User) -> RefreshToken:
        return RefreshToken.for_user(user)

    return _make_refresh_token


@pytest.fixture()
def make_access_token() -> Callable:
    def _make_access_token(user: User) -> AccessToken:
        return AccessToken.for_user(user)

    return _make_access_token


@pytest.fixture
def user_1(make_user: Callable) -> User:
    return make_user()


@pytest.fixture
def user_1_token(user_1: User) -> AccessToken:
    return AccessToken.for_user(user_1)


@pytest.fixture
def user_1_reset_password_data(user_1: User) -> Tuple[str, str]:
    uidb64 = urlsafe_base64_encode(force_bytes(user_1.pk))
    token = default_token_generator.make_token(user_1)
    return uidb64, token


@pytest.fixture()
def make_reset_password_request() -> Callable:
    """Reset password request instance fixture"""

    def _make_reset_password_request(*args: Any, **kwargs: Any) -> Code:
        return Code.objects.create(*args, **kwargs)

    return _make_reset_password_request
