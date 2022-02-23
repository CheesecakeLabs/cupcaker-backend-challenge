from typing import Any

from django.conf import settings

from api.core.messenger.base import EMAIL_TYPE, SMS_TYPE, BaseSender
from api.core.messenger.email import Email
from api.core.messenger.sms import SMS

MESSENGER_MAP = {SMS_TYPE: SMS, EMAIL_TYPE: Email}


def get_default_messenger(*args: Any, **kwargs: Any) -> BaseSender:
    """Get the default messenger service"""
    return MESSENGER_MAP[settings.DEFAULT_MESSENGER](*args, **kwargs)
