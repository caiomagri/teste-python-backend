from django.urls import path, include
from django.conf import settings

from rest_framework import routers

from .api.viewsets import UserViewSet

router = routers.DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path(settings.API_BASE_PATH, include(router.urls)),
]
