from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, IsAuthenticated

from api.serializers import PostSerializer, GroupSerializer, CommentSerializer
from posts.models import Post, Group


class OnlyAuthorChangeContent(BasePermission):
    message = 'Только автор поста может изменить контент.'

    def has_object_permission(self, request, view, obj):
        permission = request.user == obj.author or request.method == 'GET'
        return permission


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [OnlyAuthorChangeContent, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def post_obj(self):
        queryset = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return queryset

    def get_queryset(self):
        queryset = self.post_obj().comments.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.post_obj())

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого комментария запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого комментария запрещено!')
        super(CommentViewSet, self).perform_destroy(instance)
