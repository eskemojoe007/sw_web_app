from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateUserSerializer, UserSerializer
from knox.models import AuthToken


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'user': UserSerializer(user, context=self.get_serializer_context()).data,
                'token': AuthToken.objects.create(user),
            },
            status=status.HTTP_201_CREATED)
