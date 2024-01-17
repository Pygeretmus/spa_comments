from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, write_only=True)
    confirm = serializers.CharField(max_length=30, write_only=True)
    email = serializers.EmailField()

    username = serializers.CharField(max_length=30)  # django offers nonsense in swagger without

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "confirm",
        ]

    def validate(self, data):
        if data.get("password") != data.pop("confirm", None):
            raise serializers.ValidationError("Password and confirm do not match.")
        elif User.objects.filter(username=data.get("username")):
            raise serializers.ValidationError("Username already exists.")
        elif User.objects.filter(email=data.get("email")):
            raise serializers.ValidationError("Email already exists.")
        elif data.get("password"):
            data["password"] = make_password(data.get("password"))
        return data
