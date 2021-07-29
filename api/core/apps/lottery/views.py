import logging
import random

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import BetSerializer
from .scraper import get_lottery_result

# Get an instance of a logger
logger = logging.getLogger(__name__)


class LotteryResultView(APIView):

    def get(self, request, *args, **kwargs):
        result = get_lottery_result()
        return Response({"result": result}, status=status.HTTP_200_OK)


class BetView(APIView):

    def get(self, request, *args, **kwargs):
        bets = request.user.bets
        serializer = BetSerializer(bets, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        payload = request.data.copy()

        dozens = int(request.data.get("dozens", 0))

        if not (6 <= dozens <= 10):
            return Response({"erro": "O número de dezenas deve ser no mínimo 6 e no máximo 10."},
                            status=status.HTTP_400_BAD_REQUEST)

        numbers = sorted(list(random.sample(range(1, 61), dozens)))

        payload.update({
            "user": request.user.pk,
            "numbers": numbers
        })

        serializer = BetSerializer(data=payload)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BetResultView(APIView):
    def get(self, request, *args, **kwargs):
        bet = request.user.bets.all().first()
        serializer = BetSerializer(bet)

        result = get_lottery_result()
        numbers = serializer.data.get("numbers")
        right_numbers = list(set(numbers) & set(result))

        response = {
            "right_numbers": {
                "total_right": len(right_numbers),
                "numbers": right_numbers
            },
            "numbers": numbers,
            "result": result
        }
        return Response(response)
