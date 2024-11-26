from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from product.models import Product, ProductOption

# Create your models here.

class User(AbstractUser):
    # username = models.TextField() // 이미 unique=True
    password = models.TextField()
    email = models.TextField()
    phone = models.TextField(max_length=15, blank=False, null=False, default="") # blank 폼에서 빈 값으로 남겨도 유효, null 데이터베이스에 이 필드의 null값을 허용
    birth = models.DateField(null=True, blank=True, default='2000-01-01')

class UserProduct(models.Model):
    user = models.ForeignKey(
        User,  # User 모델 참조
        on_delete=models.CASCADE,
        related_name="user"
    )
    product = models.ForeignKey(
        Product,  # Product 모델 참조
        on_delete=models.CASCADE,
        related_name="product"
    )
    joined_at = models.DateTimeField(auto_now_add=True)  # 가입 날짜

    class Meta:
        unique_together = ('user', 'product')  # 동일한 사용자와 제품의 중복 방지
