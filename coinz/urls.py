from django.urls import path
from coinz import api


appname = 'coinz'
urlpatterns = [
    path('api/', api.CoinzAPI.as_view(), name='api'),
    path('api/by-week/', api.CoinzByWeekAPI.as_view(), name='api-by-week'),
    path('api/by-year/', api.CoinzByYearAPI.as_view(), name='api-by-year'),
    path('api/last-24/', api.CoinzLast24API.as_view(), name='api-last-24'),
    path('api/date-range/', api.CoinzDateRangeAPI.as_view(), name='api-date-range')
]