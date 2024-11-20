from rest_framework import serializers
from .models import User
from .models import Product, UserProduct

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'birth']  # 필요에 따라 필드를 추가할 수 있음
        read_only_fields = ['id']  # id는 읽기 전용

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone', 'birth']
        extra_kwargs = {
            'password': {'write_only': True}  # 비밀번호는 API 응답에 포함되지 않도록 설정
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            phone=validated_data.get('phone', ''),
            birth=validated_data.get('birth', '2000-01-01')  # 기본값 설정
        )
        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description']


class UserProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')

    class Meta:
        model = UserProduct
        fields = ['product_name', 'product']