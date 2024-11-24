from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status,  generics
from django.http import JsonResponse

from django.shortcuts import get_object_or_404, get_list_or_404
from django.conf import settings

from .models import Product, ProductOption, Review
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, ReviewSerializer
import requests

# API 키 및 URL 설정
API_KEY = settings.PRODUCT_API_KEY
SAVING_API_URL = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
DEPOSIT_API_URL = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"

@api_view(['GET'])
def DepositProductListView(request):
    URL = DEPOSIT_API_URL
    top_fin_grp_no_values = ['020000', '030300']  # 여러 개의 topFinGrpNo 값
    all_response_data = []  # 모든 요청의 결과를 저장할 리스트
    
    for topFinGrpNo in top_fin_grp_no_values:
        params = {
            'auth': API_KEY,
            'topFinGrpNo': topFinGrpNo,
            'pageNo': 1
        }
        response = requests.get(URL, params=params).json()
        all_response_data.append(response)  # 각 요청의 결과를 리스트에 저장

    # 응답 결과를 하나로 합침
    combined_response = {
        'message': '성공',
        'data': all_response_data  # 여러 요청의 결과를 포함
    }

    return JsonResponse(combined_response)


@api_view(['GET'])
def save_deposit_products(request):
    URL = DEPOSIT_API_URL
    top_fin_grp_no_values = ['020000', '030300']  # 여러 개의 topFinGrpNo 값
    all_response_data = []

    for topFinGrpNo in top_fin_grp_no_values:
        params = {
            'auth': API_KEY,
            'topFinGrpNo': topFinGrpNo,
            'pageNo': 1
        }
        response = requests.get(URL, params=params).json()
        all_response_data.append(response)  # 각 요청에 대한 응답 데이터를 저장

        # 상품 및 상품 옵션 처리
        for li in response['result']['baseList']:
            fin_prdt_cd = li.get('fin_prdt_cd')
            fin_co_no = li.get('fin_co_no')
            kor_co_nm = li.get('kor_co_nm')
            fin_prdt_nm = li.get('fin_prdt_nm')
            join_way = li.get('join_way')
            mtrt_int = li.get('mtrt_int', "")
            spcl_cnd = li.get('spcl_cnd', "")
            join_deny = li.get('join_deny', "")
            join_member = li.get('join_member',"")
            etc_note = li.get('etc_note', "")
            max_limit = li.get('max_limit', 0.0)

            # 이미 존재하는 상품이면 건너뛰기
            if Product.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
                continue

            save_data_pd = {
                'fin_prdt_cd': fin_prdt_cd,
                'is_saving': False,
                'fin_co_no': fin_co_no,
                'kor_co_nm': kor_co_nm,
                'fin_prdt_nm': fin_prdt_nm,
                'join_way': join_way,
                'mtrt_int': mtrt_int,
                'spcl_cnd': spcl_cnd,
                'join_deny': join_deny,
                'join_member': join_member,
                'etc_note': etc_note,
                'max_limit': max_limit
            }

            serializer_pd = DepositProductsSerializer(data=save_data_pd)
            if serializer_pd.is_valid(raise_exception=True):
                serializer_pd.save()

        # ProductOption 저장
        for li in response['result']['optionList']:
            # Product 객체 가져오기
            product = get_object_or_404(Product, fin_prdt_cd=fin_prdt_cd)
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




@api_view(['GET'])
def SavingProductListView(request):
    URL = SAVING_API_URL
    top_fin_grp_no_values = ['020000', '030300']  # 여러 개의 topFinGrpNo 값
    all_response_data = []  # 모든 요청의 결과를 저장할 리스트
    
    for topFinGrpNo in top_fin_grp_no_values:
        params = {
            'auth': API_KEY,
            'topFinGrpNo': topFinGrpNo,
            'pageNo': 1
        }
        response = requests.get(URL, params=params).json()
        all_response_data.append(response)  # 각 요청의 결과를 리스트에 저장

    # 응답 결과를 하나로 합침
    combined_response = {
        'message': '성공',
        'data': all_response_data  # 여러 요청의 결과를 포함
    }

    return JsonResponse(combined_response)



# 적금 저장하기
@api_view(['GET'])
def save_saving_products(request):
    URL = SAVING_API_URL
    top_fin_grp_no_values = ['020000', '030300']  # 여러 개의 topFinGrpNo 값
    all_response_data = []
    
    for topFinGrpNo in top_fin_grp_no_values:
        params = {
            'auth': API_KEY,
            'topFinGrpNo': topFinGrpNo,
            'pageNo': 1
        }
        response = requests.get(URL, params=params).json()
        all_response_data.append(response)  # 각 요청에 대한 응답 데이터를 저장
        
        # 상품 및 상품 옵션 처리
        for li in response['result']['baseList']:
            fin_prdt_cd = li.get('fin_prdt_cd')
            fin_co_no = li.get('fin_co_no')
            kor_co_nm = li.get('kor_co_nm')
            fin_prdt_nm = li.get('fin_prdt_nm')
            join_way = li.get('join_way')
            mtrt_int = li.get('mtrt_int', "")
            spcl_cnd = li.get('spcl_cnd', "")
            join_deny = li.get('join_deny', "")
            join_member = li.get('join_member', "")
            etc_note = li.get('etc_note', "")
            max_limit = li.get('max_limit', 0.0)

            # 이미 존재하는 상품이면 건너뛰기
            if Product.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
                continue

            save_data_pd = {
                'fin_prdt_cd': fin_prdt_cd,
                'is_saving': True,
                'fin_co_no': fin_co_no,
                'kor_co_nm' : kor_co_nm,
                'fin_prdt_nm': fin_prdt_nm,
                'join_way': join_way,
                'mtrt_int': mtrt_int,
                'spcl_cnd': spcl_cnd,
                'join_deny': join_deny,
                'join_member': join_member,
                'etc_note': etc_note,
                'max_limit': max_limit
            }

            serializer_pd = DepositProductsSerializer(data=save_data_pd)
            if serializer_pd.is_valid(raise_exception=True):
                serializer_pd.save()

        # ProductOption 저장
        for li in response['result']['optionList']:
            product = get_object_or_404(Product, fin_prdt_cd=fin_prdt_cd)
            fin_prdt_cd = li.get('fin_prdt_cd')
            intr_rate_type_nm = li.get('intr_rate_type_nm')
            rsrv_type_nm = li.get('rsrv_type_nm')
            intr_rate = li.get('intr_rate', -1) or -1
            intr_rate2 = li.get('intr_rate2', -1)
            save_trm = li.get('save_trm', 0)

            # ProductOption이 이미 존재하면 건너뛰기
            if ProductOption.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
                continue

            save_data_op = {
                'fin_prdt_cd': fin_prdt_cd,
                'is_saving': True,
                'intr_rate_type_nm': intr_rate_type_nm,
                'rsrv_type_nm': rsrv_type_nm,
                'intr_rate': intr_rate,
                'intr_rate2': intr_rate2,
                'save_trm': save_trm
            }

            serializer_op = DepositOptionsSerializer(data=save_data_op)
            if serializer_op.is_valid(raise_exception=True):
                serializer_op.save(product=product)

    return JsonResponse({'message': '저장 성공!'})

# 상품 상세 조회 API
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = DepositProductsSerializer
    lookup_field = 'fin_prdt_cd'  # URL에서 fin_prdt_cd로 조회
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        reviews = Review.objects.filter(product=instance)
        review_serializer = ReviewSerializer(reviews, many=True)
        data = serializer.data
        data['reviews'] = review_serializer.data
        return Response(data)
    

# 전체 상품 리스트 조회 API
class ProductTotalListView(generics.ListAPIView):
    queryset = Product.objects.all()  # 모든 상품을 가져옴
    serializer_class = DepositProductsSerializer  # DepositProductsSerializer를 사용


@api_view(['GET'])
def review_list(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_create(request, fin_prdt_cd):
    product = get_object_or_404(Product, fin_prdt_cd=fin_prdt_cd)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(product=product, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def review_update_delete(request, fin_prdt_cd, review_id):
    review = get_object_or_404(Review, id=review_id, product__fin_prdt_cd=fin_prdt_cd)
    
    if request.user != review.user:
        return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def product_review_list(request, fin_prdt_cd):
    # 특정 상품에 대한 리뷰만 필터링
    reviews = Review.objects.filter(product=fin_prdt_cd)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)