import boto3
from django.conf import settings
from django.contrib.auth import get_user_model

from api.core.messenger.base import SMS_TYPE, BaseSender

User = get_user_model()


class SMS(BaseSender):
    @property
    def service_type(self) -> str:
        """Get the service type string"""
        return SMS_TYPE

    def __init__(self):
        self.client = boto3.client(
            "sns",
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION,
        )

    def send(self, recipient: str, message: str, subject: str, *args, **kwargs):
        """Send the SMS"""
        self.client.publish(
            PhoneNumber=recipient, Message=message, Subject=subject, *args, **kwargs
        )

    def get_recipient(self, user: User) -> str:
        """Get the phone number of the user that will receive the SMS"""
        return user.phone_number
