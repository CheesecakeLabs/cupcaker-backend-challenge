from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt import serializers as simplejwt_serializers

from .helpers.tokens import refresh_token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
        )


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    full_name = serializers.CharField()
    password = serializers.CharField(trim_whitespace=False)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False)


class SignOutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()


class RefreshTokenSerializer(AccessTokenSerializer):
    refresh_token = serializers.CharField()


class ResetPasswordRequestCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordValidateCodeRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()


class ResetPasswordValidateCodeResponseSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(trim_whitespace=False)


class TokenRefreshSerializer(simplejwt_serializers.TokenRefreshSerializer):
    def validate(self, attrs):
        return refresh_token(attrs["refresh"])
