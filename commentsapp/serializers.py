from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Comments


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


class ReplySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = ("id", "user", "text", "home")


class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comments
        fields = ("id", "user", "text", "home", "reply", "replies")
        read_only_fields = ("id", "user")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        sorted_replies = instance.replies.all().order_by("-id")
        representation["replies"] = ReplySerializer(sorted_replies, many=True).data
        return representation
