from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt import views

from api.authentication import messages

from . import docs
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
from .use_cases import (
    ResetPasswordRequestCodeUseCase,
    ResetPasswordUseCase,
    ResetPasswordValidateCodeUseCase,
    SigninUseCase,
    SignoutUseCase,
    SignupUseCase,
)

User = get_user_model()


@extend_schema(**docs.signup)
@csrf_exempt
@api_view(("POST",))
@permission_classes((AllowAny,))
def signup(request: Request) -> Response:
    """Register a new user and return the user's data"""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = SignupUseCase().execute(**serializer.validated_data)
    return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@extend_schema(**docs.signin)
@csrf_exempt
@api_view(("POST",))
@permission_classes((AllowAny,))
def signin(request: Request) -> Response:
    """Return access and refresh token for the user if the user's email and password are correct"""
    serializer = SignInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    token_data = SigninUseCase().execute(
        email=serializer.validated_data["email"],
        password=serializer.validated_data["password"],
    )
    return Response(RefreshTokenSerializer(token_data).data, status=status.HTTP_200_OK)


@extend_schema(**docs.reset_password_request_code)
@csrf_exempt
@api_view(("POST",))
@permission_classes((AllowAny,))
def reset_password_request_code(request: Request) -> Response:
    """Send a reset password code through the application default messenger (Email/SMS)"""
    serializer = ResetPasswordRequestCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    ResetPasswordRequestCodeUseCase().execute(email=serializer.validated_data["email"])
    return Response(messages.SUCCESS, status=status.HTTP_200_OK)


@extend_schema(**docs.reset_password_validate_code)
@csrf_exempt
@api_view(("POST",))
@permission_classes((AllowAny,))
def reset_password_validate_code(request: Request) -> Response:
    """Return a reset password authentication token if the reset password code is valid"""
    serializer = ResetPasswordValidateCodeRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    uidb64, token = ResetPasswordValidateCodeUseCase().execute(
        email=serializer.validated_data["email"],
        code=serializer.validated_data["code"],
    )
    return Response(
        ResetPasswordValidateCodeResponseSerializer(
            {"uidb64": uidb64, "token": token}
        ).data,
        status=status.HTTP_200_OK,
    )


@extend_schema(**docs.reset_password)
@csrf_exempt
@api_view(("POST",))
@permission_classes((AllowAny,))
def reset_password(request: Request, uidb64: str, token: str) -> Response:
    """Set a new password to the user if the token is valid"""
    serializer = ResetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    ResetPasswordUseCase().execute(
        uidb64=uidb64, token=token, password=serializer.validated_data["password"]
    )
    return Response(messages.SUCCESS, status=status.HTTP_200_OK)


@extend_schema(**docs.refresh)
class TokenRefreshView(views.TokenRefreshView):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    serializer_class = TokenRefreshSerializer


@extend_schema(**docs.signout)
@csrf_exempt
@api_view(("POST",))
@permission_classes((IsAuthenticated,))
def signout(request: Request) -> Response:
    """Blocklist the refresh_token given in the payload"""
    serializer = SignOutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    refresh_token = serializer.data["refresh_token"]
    SignoutUseCase().execute(refresh_token)
    return Response(status=status.HTTP_204_NO_CONTENT)
