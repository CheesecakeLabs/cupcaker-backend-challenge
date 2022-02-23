from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound

from api.authentication.messages import USER_NOT_FOUND
from api.authentication.models import Code
from api.core.helpers.messenger import get_default_messenger
from api.core.use_cases.base import BaseUseCase

User = get_user_model()


class ResetPasswordRequestCodeUseCase(BaseUseCase):
    def _notify_request(self, reset_password_request: Code) -> None:
        """
        Send the password request validation code through the default messenger
        Params:
            reset_password_request: The instance with the reset password request data
        """
        sender = get_default_messenger()
        sender.send(
            recipient=sender.get_recipient(reset_password_request.user),
            subject="Password reset request",
            message=f"Hi, This is your password reset code: {reset_password_request.code}",
        )

    def _get_user_by_email(self, email: str) -> User:
        """
        Get the user by its email
        Params:
            email: The email of the user that is going to be retrieved
        Returns: The user with the email field
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise NotFound(USER_NOT_FOUND)

    def execute(self, email: str) -> None:
        """
        Create a reset password request instance and send its validation code to the user
        Params:
            email: The email address of the user that will have its password reseted
        """
        user = self._get_user_by_email(email)
        reset_password_request = Code.objects.create(
            user=user, type=Code.RESET_PASSWORD_REQUEST_TYPE
        )
        self._notify_request(reset_password_request)
