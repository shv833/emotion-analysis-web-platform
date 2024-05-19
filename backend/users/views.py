from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from groups.models import GroupStudent
from groups.serializers import GroupStudentSerializer
from users.serializers import UserSerializers


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
