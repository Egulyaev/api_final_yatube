from django.utils.text import slugify
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.response import Response

from .models import Comment, Follow, Group, Post, User
from .permission import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostGetViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    pass


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        group = self.request.query_params.get('group', None)
        if group is not None:
            queryset = queryset.filter(group=group)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )

    def get_queryset(self):
        queryset = Comment.objects.all()
        post = self.kwargs['post_id']
        queryset = queryset.filter(post=post)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(PostGetViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(slug=slugify(self.request.data))


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'following__username', ]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        return Response(status=status.HTTP_201_CREATED)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Follow.objects.filter(following=self.request.user)
            return queryset
        queryset = Follow.objects.all()
        return queryset
