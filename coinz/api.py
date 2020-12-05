from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Q, Value, Avg
from django.db.models.functions import (
    Extract, 
    Trunc, 
    Concat,
)
from coinz.serializers import CoinSerializer
from coinz.models import Coin
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz
import requests




def make_bitso_call(request):
    if request.method == "GET":
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn")
        return JsonResponse(r.json()["payload"])


class CoinzAPI(ListCreateAPIView):
    serializer_class = CoinSerializer
    queryset = Coin.objects.all()

    def post(self, request):
        serializer = CoinSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            print(serializer.errors)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class CoinzLast24API(ListAPIView):
    """
        Each record is filtered: the ones that meet the condition 
        where their "created_at" datetime value is included in the time
        difference between the current time and the last 24 hours.
    """
    serializer_class = CoinSerializer

    def list(self, request, *args, **kwargs):

        current_time = datetime.utcnow()
        time_difference = current_time - timedelta(hours=24)

        queryset = Coin.objects.filter(
            created_at__gte=time_difference
        ).order_by("created_at")

        serializer = CoinSerializer(queryset, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class CoinzByWeekAPI(ListAPIView):
    """
        Get the last month as an integer number and converts it to
        a datetime object, then records are filtered if their date is 
        inside the interval from: 
            [last month, current month]
    """
    serializer_class = CoinSerializer

    def list(self, request, *args, **kwargs):

        datetime_interval = datetime.utcnow() - timedelta(weeks=1)
        queryset = Coin.objects.filter(created_at__gte=datetime_interval).order_by("created_at")
        
        serializer = CoinSerializer(queryset, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class CoinzByMonthAPI(ListAPIView):
    """
        Get the last month as an integer number and converts it to
        a datetime object, then records are filtered if their date is 
        inside the interval from: 
            [last month, current month]
    """
    serializer_class = CoinSerializer

    def list(self, request, *args, **kwargs):
        
        last_month = datetime.utcnow() - relativedelta(months=1)
        queryset = Coin.objects.filter(created_at__gte=last_month).order_by("created_at")

        serializer = CoinSerializer(queryset, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class CoinzByYearAPI(ListAPIView):
    """
        Here I mimic the behaviour of the Bitso trade market dashboard 
        for "1yr" filter.
        * Get the records for every 7 days for each year where the
        weekday is monday.
    """
    serializer_class = CoinSerializer

    def list(self, request, *args, **kwargs):
        
        queryset = Coin.objects.annotate(weekday=Extract("created_at", "week_day")).filter(weekday=2).order_by("created_at")

        serializer = CoinSerializer(queryset, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    

class CoinzDateRangeAPI(ListAPIView):
    """
        A django query filter is used (<date>__range) to 
        specify the start date and the end date.
    """
    serializer_class = CoinSerializer

    def list(self, request, *args, **kwargs):

        date1 = request.query_params.get("date1").strip().replace("-", "/")
        date1 = datetime.strptime(date1, "%Y/%m/%d")
        date2 = request.query_params.get("date2").strip().replace("-", "/")
        date2 = datetime.strptime(date2, "%Y/%m/%d")

        queryset = Coin.objects.filter(
            created_at__range=[date1, date2]
        ).order_by("created_at")

        serializer = CoinSerializer(queryset, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )



"""
    Coin.objects.annotate(month=Extract("created_at", lookup_name="month")).values("month").annotate(count=Count("id")).values("month", "count")
    Coin.objects.annotate(date=Trunc("created_at", "week")).values("date").annotate(count=Count("id")).count()
"""