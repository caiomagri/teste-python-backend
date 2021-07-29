from django.urls import path
from django.conf import settings

from .views import LotteryResultView

urlpatterns = [
    path(f"{settings.API_BASE_PATH}lottery/results/", LotteryResultView.as_view(), name='get_lottery_result'),
]
