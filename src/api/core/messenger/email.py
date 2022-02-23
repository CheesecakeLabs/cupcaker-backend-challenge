from typing import Any
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from api.core.messenger.base import EMAIL_TYPE, BaseSender

User = get_user_model()


class Email(BaseSender):
    @property
    def service_type(self) -> str:
        """Get the service type string"""
        return EMAIL_TYPE

    def send(
        self,
        recipient: str,
        message: str,
        subject: str,
        from_email: str = settings.DEFAULT_FROM_EMAIL,
        *args: Any,
        **kwargs: Any
    ):
        """Send the email"""
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[recipient],
            fail_silently=False,
            *args,
            **kwargs
        )

    def get_recipient(self, user: User) -> str:
        """Get the email address of the user that will recieve the email"""
        return user.email
