from django.contrib.auth import get_user_model

from api.core.use_cases.base import BaseUseCase

User = get_user_model()


class SignupUseCase(BaseUseCase):
    def execute(self, **user_data: dict) -> User:
        """
        Register a new user
        Params:
            user_data: The user registration info
        Returns: The registered User instance
        """
        return User.objects.create_user(**user_data)
