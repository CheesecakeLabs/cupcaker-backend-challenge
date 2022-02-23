from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from .helpers.secrets import generate_code
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = None  # Remove username field
    email = models.EmailField(_("Email address"), unique=True)
    full_name = models.CharField(_("Full name"), max_length=60, blank=True)

    # Permissions
    is_active = models.BooleanField(_("Is active"), default=True)
    is_staff = models.BooleanField(_("Is staff"), default=False)
    is_superuser = models.BooleanField(_("Is admin"), default=False)

    # Meta
    date_joined = models.DateTimeField(_("Date joined"), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Code(TimeStampedModel):
    RESET_PASSWORD_REQUEST_TYPE = "RESET_PASSWORD_REQUEST"
    USER_CONFIRMATION_TYPE = "USER_CONFIRMATION"
    CODE_TYPES = (
        (RESET_PASSWORD_REQUEST_TYPE, RESET_PASSWORD_REQUEST_TYPE),
        (USER_CONFIRMATION_TYPE, USER_CONFIRMATION_TYPE),
    )

    user = models.ForeignKey(
        User,
        related_name="code_tokens",
        on_delete=models.CASCADE,
        verbose_name=_("The User which is associated to this"),
    )
    code = models.CharField(_("Code"), max_length=6, default=generate_code)
    type = models.CharField(_("Type"), max_length=25, choices=CODE_TYPES)
    was_used = models.BooleanField(_("Was already used?"), default=False)

    def __str__(self):
        return f"{self.user}"

    @property
    def is_eligible_for_reset(self):
        """Is code still valid?"""
        return (
            not self.was_used
            and (timezone.now() - self.created) < settings.FORGOT_TIME_EXPIRATION_TIME
        )

    class Meta:
        verbose_name = _("Code")
        ordering = ("-created",)
