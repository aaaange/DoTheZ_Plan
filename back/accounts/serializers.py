from rest_framework import serializers
from .models import User, UserProduct

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

class UserProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProduct
        fields = [
            'id',  # UserProduct 모델의 기본 키
            'user',  # User 외래 키
            'product',  # Product 외래 키
            'joined_at',  # 가입 날짜
        ]
        read_only_fields = ['joined_at']  # 자동 생성 필드