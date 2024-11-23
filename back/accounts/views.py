from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .serializers import UserSerializer, RegisterSerializer
# from .serializers import UserSerializer, RegisterSerializer, ProductSerializer, UserProductSerializer
# from .models import Product, UserProduct, User
from .models import User, UserProduct
from product.models import Product, ProductOption
from product.serializers import DepositProductsSerializer, DepositOptionsSerializer
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user:
        auth_login(request, user)
        token, created = Token.objects.get_or_create(user=user)  # 사용자에게 토큰 생성
        return Response({"message": "Login successful", "user": UserSerializer(user).data, "key": token.key }, status=status.HTTP_200_OK)
    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout(request):
    auth_logout(request)
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def signup(request):
    if request.user.is_authenticated:
        return Response({"error": "User already authenticated"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User created successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update(request):
    if not request.user.is_authenticated:
        return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User updated successfully", "user": serializer.data}, status=status.HTTP_200_OK)
    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def change_password(request):
    if not request.user.is_authenticated:
        return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    new_password = request.data.get('new_password')
    if new_password:
        request.user.set_password(new_password)
        request.user.save()
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
    return Response({"error": "New password is required"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete(request):
    if not request.user.is_authenticated:
        return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    user = request.user
    auth_logout(request)
    user.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def profile(request, user_id):
    # user_id로 사용자 객체를 가져옵니다.
    person = get_object_or_404(User, id=user_id)

    # 인증된 사용자만 접근할 수 있도록 합니다.
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    # 요청된 사용자의 정보 반환
    data = {
        'user_id': person.id,
        'username': person.username,
        'email': person.email,
        'phone': person.phone,
        'birth': person.birth,
    }

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_product_subscription(request, fin_prdt_cd):
    user = request.user  # 로그인한 사용자
    product = get_object_or_404(Product, fin_prdt_cd=fin_prdt_cd)  # 해당 금융 상품

    # 사용자가 이미 이 상품에 가입되어 있는지 확인
    user_product, created = UserProduct.objects.get_or_create(user=user, product=product)

    if not created:
        # 이미 가입한 경우, 탈퇴
        user_product.delete()
        message = '성공적으로 삭제되었습니다.'
        status_code = status.HTTP_200_OK
    else:
        # 상품에 가입한 경우
        message = '성공적으로 등록되었습니다.'
        status_code = status.HTTP_201_CREATED

    # 사용자가 가입한 금융 상품 목록을 직렬화해서 반환
    user_products = UserProduct.objects.filter(user=user)
    serializer = DepositProductsSerializer([user_product.product for user_product in user_products], many=True)

    return Response({
        'message': message,
        'user_products': serializer.data  # 가입한 금융 상품 목록
    }, status=status_code)


@api_view(['GET'])
def my_subscribed_products(request):
    user = request.user
    user_products = UserProduct.objects.filter(user=user)
    products = [user_product.product for user_product in user_products]
    serializer = DepositProductsSerializer(products, many=True)
    return Response(serializer.data)

import pandas as pd
import numpy as np
import base64
import io
from matplotlib import pyplot as plt

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subcribed_products_graph(request):
    user = request.user
    user_products = UserProduct.objects.filter(user=user)
    product_pks = [user_product.product_id for user_product in user_products]
    product_options = ProductOption.objects.filter(product=product_pks)
    
    # 데이터 준비
    product_names = [option.product.name for option in product_options]  # 제품 이름
    intr_rates = [option.intr_rate for option in product_options]  # 금리

    # 그래프 생성
    plt.figure(figsize=(10, 6))
    plt.bar(product_names, intr_rates, color='skyblue')
    plt.xlabel('Product Name')
    plt.ylabel('Interest Rate (%)')
    plt.title('Comparison of Interest Rates by Product')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # 그래프를 이미지로 변환
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()

    # 응답 반환
    return Response({"graph": image_base64})


@api_view(['POST'])
def check_username(request):
    username = request.data.get('username')
    if User.objects.filter(username=username).exists():
        return JsonResponse({'isAvailable': False})  # 중복된 아이디
    return JsonResponse({'isAvailable': True})   # 사용 가능한 아이디

@api_view(['GET'])
def user_info(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'username': request.user.username,
            'is_authenticated': True,
            'pk': request.user.pk  # 사용자의 pk 추가
        })