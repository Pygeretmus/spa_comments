from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Comments
from .permissions import IsOwnerOrAuthenticated, IsOwnerOrAuthenticatedOrPost
from .serializers import CommentSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default create(), , update(), partial_update()
    and destroy() actions. retrieve() and list() actions caching for 1 minute.
    """

    queryset = User.objects.exclude(is_staff=True)
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAuthenticatedOrPost]

    @method_decorator(cache_page(60 * 1))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 1))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentsViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default create(), , update(), partial_update()
    and destroy() actions. retrieve() and list() actions caching for 1 minute.
    """

    queryset = Comments.objects.all().order_by("-id")
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @method_decorator(cache_page(60 * 1))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 1))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
