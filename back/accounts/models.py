from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    # username = models.TextField() // 이미 unique=True
    password = models.TextField()
    email = models.TextField()
    phone = models.TextField(max_length=15, blank=False, null=False, default="") # blank 폼에서 빈 값으로 남겨도 유효, null 데이터베이스에 이 필드의 null값을 허용
    birth = models.DateField(null=True, blank=True, default='2000-01-01')


