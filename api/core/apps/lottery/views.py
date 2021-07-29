import json
import logging

from django.http import HttpResponse
from rest_framework.views import APIView

from .scraper import get_lottery_result

# Get an instance of a logger
logger = logging.getLogger(__name__)


class LotteryResultView(APIView):
    def get(self, request, *args, **kwargs):
        result = get_lottery_result()

        return HttpResponse(
            json.dumps({"result": result}),
            status=200,
            content_type="application/json")
