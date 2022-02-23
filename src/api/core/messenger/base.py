from abc import ABC, abstractmethod
from typing import Any

from django.contrib.auth import get_user_model

User = get_user_model()

EMAIL_TYPE = "EMAIL"
SMS_TYPE = "SMS"


class BaseSender(ABC):
    @property
    @abstractmethod
    def service_type(self) -> str:
        """Get the messeger service name"""
        pass

    @abstractmethod
    def send(
        self, recipient: str, message: str, subject: str, *args: Any, **kwargs: Any
    ) -> None:
        """Send the message"""
        pass

    @abstractmethod
    def get_recipient(self, user: User, *args: Any, **kwargs: Any) -> str:
        """Get the address that will receive the message"""
        pass
