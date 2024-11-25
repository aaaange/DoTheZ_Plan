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

# 가장 최근 영업일 데이터 가져오기 (중복 제거를 위한 함수화)
def get_recent_exchange_date(search_date, base_url, params):
    while True:
        response = requests.get(base_url, params=params, verify=False)
        if response.status_code == 200:
            response_data = response.json()
            if response_data:
                return response_data, search_date
        # 영업일이 아닐 경우 하루 전 날짜로 요청
        now = datetime.strptime(search_date, '%Y-%m-%d')
        search_date = now - timedelta(days=1)
        search_date = change_date_format(str(search_date).split()[0])
        params['searchdate'] = search_date

# 환율 api로 데이터를 받아서 DB에 저장
def save_exchange_rate(search_date):
    EXCHANGE_API_KEY = settings.EXCHANGE_API_KEY
    if not EXCHANGE_API_KEY:
        raise ValueError("API 키가 설정되지 않았습니다.")  # API 키 유효성 검사 추가
    base_url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
    search_date = change_date_format(search_date)
    params = {
        'authkey': EXCHANGE_API_KEY,
        'data': 'AP01',
        'searchdate': search_date
    }

    # response = requests.get(base_url, params=params).json()
    # 비영엽일이거나 11시 이전이라 데이터가 null로 받아지는 경우 -> 하루 전, 또는 영업일의 데이터를 받을 때까지 1일씩 빼서 요청을 보냄
    # 수정: 공통 함수로 영업일 데이터 가져오기 처리
    response_data, search_date = get_recent_exchange_date(search_date, base_url, params)

    product_keys = ['search_date', 'cur_unit', 'cur_nm', 'deal_bas_r']

    if not ExchangeRate.objects.filter(search_date=search_date).exists():
        for item in response_data:
            save_data = {key: (search_date if key == 'search_date' else item[key]) for key in product_keys}
            serializer = ExchangeRateSerializer(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()


@api_view(['GET'])
def exchange_rate(request):
    search_date = request.GET['searchDate']
    country_from = request.GET['from']
    country_to = request.GET['to']

    # API 키 및 기본 URL 설정
    EXCHANGE_API_KEY = settings.EXCHANGE_API_KEY
    if not EXCHANGE_API_KEY:
        return Response({"error": "API 키가 설정되지 않았습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    base_url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
    params = {
        'authkey': EXCHANGE_API_KEY,
        'data': 'AP01',
        'searchdate': search_date
    }

    # DB에 해당 날짜의 데이터가 없을 경우 가져와서 저장
    if not ExchangeRate.objects.filter(search_date=search_date).exists():
        save_exchange_rate(search_date)
    
    # 환율 정보 조회
    response_data, search_date = get_recent_exchange_date(search_date, base_url, params)

    # 필터링된 환율 데이터 가져오기
    exchange_rates = ExchangeRate.objects.filter(search_date=search_date, cur_unit__in=[country_from, country_to])

    if exchange_rates.exists():
        serializer = ExchangeRateSerializer(exchange_rates, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "해당 날짜의 데이터를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)



