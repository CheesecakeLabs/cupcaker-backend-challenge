from django.utils.translation import gettext_lazy as _

EMAIL_ALREADY_REGISTERED = _(
    "This e-mail address is already associated with an account."
)
WRONG_CREDENTIALS = _("Incorrect authentication credentials.")
INVALID_ACCESS_TOKEN = _("Invalid or expired access token.")
RESET_PASSWORD_REQUEST_NOT_FOUND = _("Password request was not found")
RESET_PASSWORD_SUBMIT_INVALID_CODE = _("The code is expired or has already been used")
USER_NOT_FOUND = _("User not found")
SUCCESS = _("Success")
