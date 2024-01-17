from django.contrib.auth.models import User
from rest_framework import viewsets

from .permissions import IsOwnerOrAuthenticated
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    queryset = User.objects.exclude(is_staff=True)
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAuthenticated]
