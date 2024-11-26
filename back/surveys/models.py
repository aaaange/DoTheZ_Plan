from django.db import models
from accounts.models import User

# Create your models here.
class UserSurvey(models.Model):
    id = models.AutoField(primary_key=True)  # PK
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # FK, User 테이블의 ID를 참조
    created_at = models.DateTimeField(auto_now_add=True)  # 설문 제출일
    deposit_or_saving = models.BooleanField()  # 예금/적금
    minimum_deposit = models.FloatField()  # 최소 예치금/월 최소 투자 금액
    investment_period = models.FloatField()  # 투자 기간
    expected_return = models.FloatField()  # 요구 수익률
    interest_rate_type = models.CharField(  # 저축 금리 유형 (단리/복리)
        max_length=10,
        choices=[
            ("단리", "단리"),
            ("복리", "복리"),
        ]
    )
    investment_goal = models.CharField(  # 투자 목적
        max_length=20,
        choices=[
            ("결혼자금", "결혼자금"),
            ("주택마련", "주택마련"),
            ("노후준비", "노후준비"),
        ]
    )
    spending_habit_1 = models.CharField(  # 소비 습관 1
        max_length=10,
        choices=[
            ("쇼핑", "쇼핑"),
            ("여가", "여가"),
            ("식비", "식비"),
            ("교통", "교통"),
            ("주거", "주거"),
            ("저축", "저축"),
            ("기타", "기타"),
        ]
    )
    spending_habit_2 = models.CharField(  # 소비 습관 2
        max_length=10,
        choices=[
            ("쇼핑", "쇼핑"),
            ("여가", "여가"),
            ("식비", "식비"),
            ("교통", "교통"),
            ("주거", "주거"),
            ("저축", "저축"),
            ("기타", "기타"),
        ]
    )
    spending_habit_3 = models.CharField(  # 소비 습관 3
        max_length=10,
        choices=[
            ("쇼핑", "쇼핑"),
            ("여가", "여가"),
            ("식비", "식비"),
            ("교통", "교통"),
            ("주거", "주거"),
            ("저축", "저축"),
            ("기타", "기타"),
        ]
    )
    fixed_income = models.FloatField()  # 고정 수입
    main_bank = models.CharField(max_length=50)  # 주 거래 은행
    household_type = models.CharField(  # 가구 유형
        max_length=10,
        choices=[
            ("1인가구", "1인가구"),
            ("2인가구", "2인가구"),
            ("4인 이상", "4인 이상"),
        ]
    )
    age = models.IntegerField()  # 만 나이
    risk_tolerance = models.CharField(  # 위험 성향
        max_length=20,
        choices=[
            ("낮음", "낮음"),
            ("보통", "보통"),
            ("높음", "높음"),
        ]
    )

    current_assets = models.IntegerField()  # 현재 자산

