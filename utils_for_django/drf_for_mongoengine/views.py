from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.response import Response
from .models import MongoToken


class ObtainMongoAuthToken(ObtainAuthToken):
    model = MongoToken

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created = self.model.objects.get_or_create(user=serializer.object['user'])
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


obtain_mongo_auth_token = ObtainMongoAuthToken.as_view()