from django.urls import path
from django.conf import settings

from .views import LotteryResultView, BetView, BetResultView

urlpatterns = [
    path(f"{settings.API_BASE_PATH}lottery/results/", LotteryResultView.as_view(), name='lottery_result'),
    path(f"{settings.API_BASE_PATH}lottery/bets/", BetView.as_view(), name='bets'),
    path(f"{settings.API_BASE_PATH}lottery/bets/result", BetResultView.as_view(), name='last_bet_result'),
]
