from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.exceptions import InvalidToken

from apps.pkg.encrypto.encryption import decrypt

User = get_user_model()


class CustomAuthentication(JWTAuthentication):

    def get_validated_token(self, raw_token: bytes) -> Token:
        try:
            token = decrypt(encrypted=raw_token, key=settings.ENCRYPT_KEY)
        except ValueError:
            raise InvalidToken(
                {
                    "detail": _("Given token not valid for any token type"),
                }
            )
        return super().get_validated_token(token.encode())

    def get_user(self, validated_token: Token) -> AuthUser:
        user = User(
            id=validated_token["user_id"],
            username=validated_token["username"],
            email=validated_token["email"],
        )

        return user
