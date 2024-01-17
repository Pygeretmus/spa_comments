from django.contrib.auth.models import User
from rest_framework import viewsets

from .models import Comments
from .permissions import IsOwnerOrAuthenticatedOrPost, IsOwnerOrAuthenticated
from .serializers import CommentSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    queryset = User.objects.exclude(is_staff=True)
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAuthenticatedOrPost]


class CommentsViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
