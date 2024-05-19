from rest_framework import serializers
from .models import Group, GroupStudent
from users.serializers import UserPublicInfoSerializer


class GroupStudentSerializer(serializers.ModelSerializer):
    student = UserPublicInfoSerializer()

    class Meta:
        model = GroupStudent
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    students = GroupStudentSerializer("students", many=True, read_only=True)

    class Meta:
        model = Group
        fields = "__all__"
