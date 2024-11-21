from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse

from django.shortcuts import get_object_or_404, get_list_or_404
from django.conf import settings

from .models import Product, ProductOption
from .serializers import DepositProductsSerializer, DepositOptionsSerializer
import requests

# API 키 및 URL 설정
API_KEY = settings.PRODUCT_API_KEY
SAVING_API_URL = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
DEPOSIT_API_URL = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"

@api_view(['GET'])
def ProductListView(request):
    URL = DEPOSIT_API_URL
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    response = requests.get(URL, params=params).json()
    return JsonResponse({'response': response})

@api_view(['GET'])
def save_deposit_products(request):
    URL = DEPOSIT_API_URL
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    response = requests.get(URL, params=params).json()
    
    # Product 모델에서 데이터가 없으면 저장
    for li in response['result']['baseList']:
        fin_prdt_cd = li.get('fin_prdt_cd')
        fin_co_no = li.get('fin_co_no')
        fin_prdt_nm = li.get('fin_prdt_nm')
        join_way = li.get('join_way')
        mtrt_int = li.get('mtrt_int', "")
        spcl_cnd = li.get('spcl_cnd', "")
        join_deny = li.get('join_deny', "")
        etc_note = li.get('etc_note', "")
        max_limit = li.get('max_limit', 0.0)

        # 이미 존재하는 상품이면 건너뛰기
        if Product.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            continue
        
        save_data_pd = {
            'fin_prdt_cd': fin_prdt_cd,
            'is_saving': False,
            'fin_co_no': fin_co_no,
            'fin_prdt_nm': fin_prdt_nm,
            'join_way': join_way,
            'mtrt_int': mtrt_int,
            'spcl_cnd': spcl_cnd,
            'join_deny': join_deny,  # join_deny는 문자열로 전달
            'etc_note': etc_note,
            'max_limit': max_limit
        }

        serializer_pd = DepositProductsSerializer(data=save_data_pd)
        if serializer_pd.is_valid(raise_exception = True):
            serializer_pd.save()
    
    # ProductOption 저장
    for li in response['result']['optionList']:
        product = get_object_or_404(Product, fin_prdt_cd=fin_prdt_cd)
        Product.objects.get(fin_prdt_cd=fin_prdt_cd)
        fin_prdt_cd = li.get('fin_prdt_cd')
        intr_rate_type_nm = li.get('intr_rate_type_nm')
        intr_rate = li.get('intr_rate', -1) or -1
        intr_rate2 = li.get('intr_rate2', -1)
        save_trm = li.get('save_trm', 0)

        # ProductOption이 이미 존재하면 건너뛰기
        if ProductOption.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            continue

        save_data_op = {
            'fin_prdt_cd': fin_prdt_cd,  
            'is_saving': False,
            'intr_rate_type_nm': intr_rate_type_nm,
            'intr_rate': intr_rate,
            'intr_rate2': intr_rate2,
            'save_trm': save_trm
        }

        serializer_op = DepositOptionsSerializer(data=save_data_op)
        if serializer_op.is_valid(raise_exception=True):
            serializer_op.save(product=product)

    return JsonResponse({'message': '저장 성공!'})
