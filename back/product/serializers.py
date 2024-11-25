from rest_framework import serializers
from .models import Product, ProductOption, Review
from accounts.serializers import UserSerializer

class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class DepositOptionsSerializer(serializers.ModelSerializer):
    product = DepositProductsSerializer(read_only=True)
    class Meta:
        model = ProductOption
        fields = '__all__'
        read_only_fields = ('product',)
        
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('product','user',)