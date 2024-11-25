from rest_framework import serializers
from .models import UserSurvey
from accounts.models import User

class UserSurveySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # user 필드는 ForeignKey로 연결되므로 PrimaryKey로 처리

    class Meta:
        model = UserSurvey
        fields = '__all__'
        read_only_fields = ('id',)
