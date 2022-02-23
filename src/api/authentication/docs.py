from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from rest_framework import status

from api.authentication import messages

from .serializers import (
    RefreshTokenSerializer,
    ResetPasswordRequestCodeSerializer,
    ResetPasswordSerializer,
    ResetPasswordValidateCodeRequestSerializer,
    ResetPasswordValidateCodeResponseSerializer,
    SignInSerializer,
    SignOutSerializer,
    SignUpSerializer,
    TokenRefreshSerializer,
    UserSerializer,
)

authentication_tag = "Authentication"

NOT_FOUND_RESPONSE = OpenApiExample(
    "Not Found",
    value={"detail": messages.USER_NOT_FOUND},
    response_only=True,
    status_codes=["404"],
)

SUCCESS_RESPONSE = OpenApiExample(
    "Success",
    value=messages.SUCCESS,
    response_only=True,
    status_codes=["200"],
)

WRONG_CREDENTIALS_RESPONSE = OpenApiExample(
    messages.WRONG_CREDENTIALS,
    value={"detail": messages.WRONG_CREDENTIALS},
    response_only=True,
    status_codes=["401"],
)

INVALID_ACCESS_TOKEN_RESPONSE = OpenApiExample(
    messages.INVALID_ACCESS_TOKEN,
    value={"detail": messages.INVALID_ACCESS_TOKEN},
    response_only=True,
    status_codes=["401"],
)

BLOCKLISTED_TOKEN_RESPONSE = OpenApiExample(
    "Token is blocklisted",
    value={"detail": "Token is blocklisted"},
    response_only=True,
    status_codes=["401"],
)

INVALID_RESET_PASSWORD_CODE_RESPONSE = OpenApiExample(
    messages.RESET_PASSWORD_SUBMIT_INVALID_CODE,
    value={"detail": messages.RESET_PASSWORD_SUBMIT_INVALID_CODE},
    response_only=True,
    status_codes=["403"],
)

RESET_PASSWORD_REQUEST_NOT_FOUND_RESPONSE = OpenApiExample(
    messages.RESET_PASSWORD_REQUEST_NOT_FOUND,
    value={"detail": messages.RESET_PASSWORD_REQUEST_NOT_FOUND},
    response_only=True,
    status_codes=["404"],
)


signup = {
    "request": SignUpSerializer,
    "responses": {status.HTTP_200_OK: UserSerializer},
    "summary": "Sign up",
    "tags": [authentication_tag],
}


signin = {
    "request": SignInSerializer,
    "responses": {
        status.HTTP_200_OK: RefreshTokenSerializer,
        status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
    },
    "summary": "Sign in",
    "tags": [authentication_tag],
    "examples": [WRONG_CREDENTIALS_RESPONSE],
}

signout = {
    "methods": ["POST"],
    "request": SignOutSerializer,
    "responses": {
        status.HTTP_204_NO_CONTENT: None,
        status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
    },
    "summary": "Sign out",
    "tags": [authentication_tag],
    "examples": [INVALID_ACCESS_TOKEN_RESPONSE],
}

refresh = {
    "methods": ["POST"],
    "request": TokenRefreshSerializer,
    "responses": {
        status.HTTP_200_OK: RefreshTokenSerializer,
        status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
    },
    "summary": "Refresh Token",
    "tags": [authentication_tag],
    "examples": [BLOCKLISTED_TOKEN_RESPONSE],
}


reset_password_request_code = {
    "request": ResetPasswordRequestCodeSerializer,
    "responses": {
        status.HTTP_200_OK: OpenApiTypes.STR,
        status.HTTP_404_NOT_FOUND: OpenApiTypes.OBJECT,
    },
    "summary": "Reset password request code",
    "tags": [authentication_tag],
    "examples": [
        SUCCESS_RESPONSE,
        NOT_FOUND_RESPONSE,
    ],
}

reset_password_validate_code = {
    "request": ResetPasswordValidateCodeRequestSerializer,
    "responses": {
        status.HTTP_200_OK: ResetPasswordValidateCodeResponseSerializer,
        status.HTTP_403_FORBIDDEN: OpenApiTypes.OBJECT,
        status.HTTP_404_NOT_FOUND: OpenApiTypes.OBJECT,
    },
    "summary": "Reset password validate code",
    "tags": [authentication_tag],
    "examples": [
        INVALID_RESET_PASSWORD_CODE_RESPONSE,
        RESET_PASSWORD_REQUEST_NOT_FOUND_RESPONSE,
    ],
}

reset_password = {
    "request": ResetPasswordSerializer,
    "responses": {
        status.HTTP_200_OK: OpenApiTypes.STR,
        status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
    },
    "summary": "Reset password",
    "tags": [authentication_tag],
    "examples": [SUCCESS_RESPONSE, WRONG_CREDENTIALS_RESPONSE],
}
