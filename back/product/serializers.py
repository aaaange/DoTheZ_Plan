from rest_framework import serializers
from .models import Product, ProductOption

class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = '__all__'
        read_only_fields = ('product',)
        
        
