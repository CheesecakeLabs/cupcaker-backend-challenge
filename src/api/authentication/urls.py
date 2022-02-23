from django.urls import path

from . import views

app_name = "auth"

urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("refresh", views.TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "reset-password/request-code",
        views.reset_password_request_code,
        name="reset-password-request-code",
    ),
    path(
        "reset-password/validate-code",
        views.reset_password_validate_code,
        name="reset-password-validate-code",
    ),
    path(
        "reset-password/<str:uidb64>/<str:token>",
        views.reset_password,
        name="reset-password",
    ),
]
