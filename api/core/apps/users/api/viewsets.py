import logging

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        if not request.data:
            return Response({"erro": "Nenhuma informação enviada."},
                            status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        password = request.data.get('password')
        old_password = request.data.get('old_password')

        if password:
            if not old_password:
                return Response({"erro": "Para alterar sua senha informe sua senha atual."},
                                status=status.HTTP_400_BAD_REQUEST)
            elif not instance.check_password(old_password):
                return Response({"erro": "Sua senha atual não é válida."},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
