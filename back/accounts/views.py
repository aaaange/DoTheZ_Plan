from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .serializers import UserSerializer, RegisterSerializer, ProductSerializer, UserProductSerializer
from .models import Product, UserProduct, User
from django.http import JsonResponse



@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user:
        auth_login(request, user)
        return Response({"message": "Login successful", "user": UserSerializer(user).data}, status=status.HTTP_200_OK)
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
def profile(request):
    person = request.user
    if not person.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
    data = {
        'user_id': person.id,
        'username': person.username,
        'email': person.email,
        'phone': person.phone,
        'birth': person.birth,
        'first_name': person.first_name,
        'last_name': person.last_name,
        'date_joined': person.date_joined,
        'is_active': person.is_active
    }
    
    return Response(data)


@api_view(['POST'])
def toggle_product_subscription(request, product_pk):
    user = request.user  # 로그인한 사용자
    product = get_object_or_404(Product, pk=product_pk)  # 해당 금융 상품

    # 사용자가 이미 이 상품에 가입되어 있는지 확인
    user_product, created = UserProduct.objects.get_or_create(user=user, product=product)

    if not created:
        # 이미 가입한 경우, 탈퇴
        user_product.delete()
        message = 'Successfully unsubscribed from the product.'
        status_code = status.HTTP_200_OK
    else:
        # 상품에 가입한 경우
        message = 'Successfully subscribed to the product.'
        status_code = status.HTTP_201_CREATED

    # 사용자가 가입한 금융 상품 목록을 직렬화해서 반환
    user_products = UserProduct.objects.filter(user=user)
    serializer = ProductSerializer([user_product.product for user_product in user_products], many=True)

    return Response({
        'message': message,
        'user_products': serializer.data  # 가입한 금융 상품 목록
    }, status=status_code)

@api_view(['GET'])
def my_subscribed_products(request):
    user = request.user
    user_products = UserProduct.objects.filter(user=user)
    products = [user_product.product for user_product in user_products]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def check_username(request):
    username = request.data.get('username')
    if User.objects.filter(username=username).exists():
        return JsonResponse({'isAvailable': False})  # 중복된 아이디
    return JsonResponse({'isAvailable': True})   # 사용 가능한 아이디


@api_view(['GET'])
def check_auth(request):
    if request.user.is_authenticated:
        return JsonResponse({'is_authenticated': True, 'username': request.user.username})
    return JsonResponse({'is_authenticated': True})
