from typing import Tuple

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.exceptions import NotFound, PermissionDenied

from api.authentication.messages import (
    RESET_PASSWORD_REQUEST_NOT_FOUND,
    RESET_PASSWORD_SUBMIT_INVALID_CODE,
)
from api.authentication.models import Code
from api.core.use_cases.base import BaseUseCase

User = get_user_model()


class ResetPasswordValidateCodeUseCase(BaseUseCase):
    def _get_reset_password_request(self, email: str, code: str) -> Code:
        """
        Get The reset password request by its email and code
        Params:
            email: the reset password request user's email
            code: the reset password request code
        Returns: The Reset password request with matching user and code
        """
        reset_password_request = Code.objects.filter(
            user__email=email,
            code=code,
            type=Code.RESET_PASSWORD_REQUEST_TYPE,
        ).first()
        if not reset_password_request:
            raise NotFound(RESET_PASSWORD_REQUEST_NOT_FOUND)
        if not reset_password_request.is_eligible_for_reset:
            raise PermissionDenied(RESET_PASSWORD_SUBMIT_INVALID_CODE)
        return reset_password_request

    def _set_reset_password_request_used(self, reset_password_request: Code) -> Code:
        """
        Set password request as used
        Params:
            reset_password_request: the reset password request
        Returns: The updated reset_password_request instance
        """
        reset_password_request.was_used = True
        reset_password_request.save()
        return reset_password_request

    def _get_user_reset_password_auth_data(self, user: User):
        """
        Get the user request password authentication data
        Params:
            user: The user that will have its password reset
        Returns: tuple containing its unique id encoded in 64 bits and an authentication token
        """
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        return uidb64, token

    def execute(self, email: str, code: str) -> Tuple[str, str]:
        """
        Get password reset authentication data if a reset password request instance exists
        and is eligible for reset
        Params:
            email: The email of the user that will have its password reseted
            code: The code that was sent through Email / SMS that will validate the user
        Returns: A tuple with the user encrypted primary key and a token for its authentication
        """
        reset_password_request = self._get_reset_password_request(email, code)
        reset_password_request = self._set_reset_password_request_used(
            reset_password_request
        )
        user = reset_password_request.user
        return self._get_user_reset_password_auth_data(user)
