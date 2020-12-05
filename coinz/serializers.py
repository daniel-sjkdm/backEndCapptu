from rest_framework import serializers
from coinz.models import Coin



class CoinSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S")
    class Meta:
        model = Coin
        fields = [
            "id",
            "created_at",
            "volume",
            "high",
            "low",
            "last",
            "vwap",
            "ask",
            "bid"
        ]