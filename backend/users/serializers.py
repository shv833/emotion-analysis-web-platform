from rest_framework import serializers
from .models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "phone_number",
            "first_name",
            "last_name",
            "email",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserPublicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "avatar", "username", "first_name", "last_name"]
