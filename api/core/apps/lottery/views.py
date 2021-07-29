import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .scraper import get_lottery_result

# Get an instance of a logger
logger = logging.getLogger(__name__)


class LotteryResultView(APIView):
    
    def get(self, request, *args, **kwargs):
        result = get_lottery_result()
        return Response({"result": result}, status=status.HTTP_200_OK)
