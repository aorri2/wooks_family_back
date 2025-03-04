from rest_framework.generics import CreateAPIView
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from users.models import CustomUser
from users.serializers import UserSerializer

# Create your views here.


class UserRegistrationView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permisson_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)
