from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer
from knox.models import AuthToken


class AuthMixin(object):
    success_status = status.HTTP_200_OK

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_user(serializer)
        return Response(
            {
                'user': UserSerializer(user, context=self.get_serializer_context()).data,
                'token': AuthToken.objects.create(user),
            },
            status=self.success_status)


class RegistrationAPI(generics.GenericAPIView, AuthMixin):
    serializer_class = CreateUserSerializer
    success_status = status.HTTP_201_CREATED

    def get_user(self, serializer):
        return serializer.save()


class LoginAPI(generics.GenericAPIView, AuthMixin):
    serializer_class = LoginUserSerializer
    success_status = status.HTTP_200_OK

    def get_user(self, serializer):
        return serializer.validated_data


class UserAPI(generics.RetreiveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
