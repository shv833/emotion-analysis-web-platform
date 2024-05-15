from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User
from users.serializers import UserSerializers


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [AllowAny]
