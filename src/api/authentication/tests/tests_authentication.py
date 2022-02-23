from typing import Callable

from api.authentication.helpers.tokens import AccessToken, JWTAuthentication


def test_jwtauthentication_get_user_returns_complete_user(
    make_user: Callable, make_access_token: Callable
) -> None:
    """Check if JWT get_user function retrieves the user instance"""
    user = make_user()
    expected_access_token = make_access_token(user)

    jwt_auth = JWTAuthentication()
    access_token = AccessToken(str(expected_access_token))

    token_user = jwt_auth.get_user(access_token)

    assert str(token_user.id) == str(user.id)
    assert token_user.email == user.email
    assert token_user.full_name == user.full_name
