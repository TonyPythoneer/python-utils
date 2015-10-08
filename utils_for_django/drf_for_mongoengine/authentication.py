from rest_framework.authentication import TokenAuthentication
from .models import MongoToken
from rest_framework import exceptions


class MongoTokenAuthentication(TokenAuthentication):
    model = MongoToken

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key.decode('UTF-8'))
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        return (token.user, token)