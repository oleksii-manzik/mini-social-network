from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from msn_app.models import Post, Like, User
from msn_app.serializers import (UserSerializerGetData,
                                 UserSerializerManipulateData, PostSerializer,
                                 LikeSerializer)
from msn_app.permissions import (IsSameUserAsAuthenticated,
                                 IsObjectOwner, IsNotAuthenticated)

MANIPULATING_DATA_ACTIONS = ('update', 'partial_update', 'destroy')
CREATE_DATA_ACTIONS = ('create',)
GET_DATA_ACTIONS = ('list', 'retrieve')


class UserView(viewsets.ModelViewSet):
    """Return user info"""
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in MANIPULATING_DATA_ACTIONS \
                or self.action in CREATE_DATA_ACTIONS:
            return UserSerializerManipulateData
        else:
            return UserSerializerGetData

    def get_permissions(self):
        permission_classes = []
        if self.action in MANIPULATING_DATA_ACTIONS:
            permission_classes.append(IsSameUserAsAuthenticated())
        elif self.action in CREATE_DATA_ACTIONS:
            permission_classes.append(IsNotAuthenticated())
        elif self.action in GET_DATA_ACTIONS:
            permission_classes.append(AllowAny())
        return permission_classes


class PostView(viewsets.ModelViewSet):
    """Return posts of authenticated user"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options',
                         'trace']

    def get_permissions(self):
        permission_classes = []
        if self.action in MANIPULATING_DATA_ACTIONS:
            permission_classes.append(IsObjectOwner())
        elif self.action in CREATE_DATA_ACTIONS:
            permission_classes.append(IsAuthenticated())
        elif self.action in GET_DATA_ACTIONS:
            permission_classes.append(AllowAny())
        return permission_classes

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeView(viewsets.ModelViewSet):
    """Return likes of authenticated user"""
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    http_method_names = ['get', 'post', 'head', 'options', 'trace']

    def get_permissions(self):
        permission_classes = []
        if self.action in MANIPULATING_DATA_ACTIONS:
            permission_classes.append(IsObjectOwner())
        elif self.action in CREATE_DATA_ACTIONS:
            permission_classes.append(IsAuthenticated())
        elif self.action in GET_DATA_ACTIONS:
            permission_classes.append(AllowAny())
        return permission_classes

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
