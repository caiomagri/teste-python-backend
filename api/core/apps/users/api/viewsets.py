import logging

from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer

logger = logging.getLogger(__name__)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny()]
        return super(UserViewSet, self).get_permissions()
