from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import status

import requests
from .models import ExchangeRate
from .serializers import ExchangeRateSerializer
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from datetime import datetime, timedelta


def change_date_format(input_date):
    date_object = datetime.strptime(input_date, '%Y-%m-%d')
    output_date = date_object.strftime('%Y-%m-%d')
    return output_date

# 환율 api로 데이터를 받아서 DB에 저장
def save_exchange_rate(search_date):
    EXCHANGE_API_KEY = settings.EXCHANGE_API_KEY
    base_url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
    search_date = change_date_format(search_date)
    params = {
        'authkey': EXCHANGE_API_KEY,
        'data': 'AP01',
        'searchdate': search_date
    }

    response = requests.get(base_url, params=params).json()
    # 비영엽일이거나 11시 이전이라 데이터가 null로 받아지는 경우 -> 하루 전, 또는 영업일의 데이터를 받을 때까지 1일씩 빼서 요청을 보냄
    while not response:
        now = datetime.strptime(search_date, '%Y-%m-%d')
        search_date = now - timedelta(days=1)
        search_date = change_date_format(str(search_date).split()[0])
        params = {
        'authkey': EXCHANGE_API_KEY,
        'data': 'AP01',
        'searchdate': search_date
        }
        response = requests.get(base_url, params=params).json()

    product_keys = ['search_date', 'cur_unit', 'cur_nm', 'deal_bas_r']

    if not ExchangeRate.objects.filter(search_date=search_date).exists():
        for item in response:
            save_data = {}
            for key in product_keys:
                if key == 'search_date':
                    save_data[key] = search_date
                else:
                    save_data[key] = item[key]

            serializer = ExchangeRateSerializer(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

    return


@api_view(['GET'])
def exchange_rate(request):
    search_date = request.GET['searchDate']
    country_from = request.GET['from']
    country_to = request.GET['to']

    # DB에 해당 날짜의 데이터가 없다 => 가져와서 저장 : save_exchange_rate
    # 비영업일이거나 영업 이전 시간이다 => 가장 최근의 이전 영업일 데이터 가져와서 저장 (save_exchange_rate 내부에서 처리)
    if not ExchangeRate.objects.filter(search_date=search_date):
        save_exchange_rate(search_date)
        
    exchange_rates = ExchangeRate.objects.filter(search_date=search_date, cur_unit__in=['KRW', country_from, country_to])
    # 비영업일이거나 영업 이전 시간이다 => 가장 최근의 이전 영업일 데이터 가져오기
    while not exchange_rates.exists():
        now = datetime.strptime(search_date, '%Y-%m-%d')
        search_date = now - timedelta(days=1)
        search_date = change_date_format(str(search_date).split()[0])
        exchange_rates = ExchangeRate.objects.filter(search_date=search_date, cur_unit__in=['KRW', country_from, country_to])

    serialize = ExchangeRateSerializer(exchange_rates, many=True)
    return Response(serialize.data, status=status.HTTP_200_OK)


