from rest_framework import serializers
from .models import UserSurvey

class UserSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSurvey
        fields = [
            'user_id',
            'deposit_or_saving',
            'minimum_deposit',
            'investment_period',
            'expected_return',
            'interest_rate_type',
            'investment_goal',
            'spending_habit_1',
            'spending_habit_2',
            'spending_habit_3',
            'fixed_income',
            'main_bank',
            'household_type',
            'age',
            'risk_tolerance',
            'current_assets',
        ]

    def validate(self, data):
        # 모든 필드가 존재하는지 검사
        missing_fields = [field for field in self.fields if field not in data]
        if missing_fields:
            raise serializers.ValidationError({f: "This field is required." for f in missing_fields})
        
        # 추가 검증 조건 (예: 최소값, 논리적 조건 등)
        if data['minimum_deposit'] <= 0:
            raise serializers.ValidationError({"minimum_deposit": "Minimum deposit must be greater than 0."})
        if data['investment_period'] <= 0:
            raise serializers.ValidationError({"investment_period": "Investment period must be greater than 0."})
        if data['expected_return'] < 0:
            raise serializers.ValidationError({"expected_return": "Expected return cannot be negative."})
        return data
