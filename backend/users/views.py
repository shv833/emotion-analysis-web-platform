from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from groups.models import GroupStudent
from groups.serializers import GroupStudentSerializer
from users.serializers import UserSerializers
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [AllowAny]


class StudentListView(generics.ListAPIView):
    queryset = GroupStudent.objects.all()
    serializer_class = GroupStudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if User.TEACHER in user.role:
            return self.queryset.filter(group__teacher=user)
        elif User.SUPERVISOR in user.role:
            return self.queryset.filter(group__supervisor=user)
        else:
            return GroupStudent.objects.none()


class LogoutView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, TokenError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
