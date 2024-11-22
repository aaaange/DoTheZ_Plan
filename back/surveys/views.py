from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserSurvey
from .serializers import UserSurveySerializer


@api_view(['GET', 'POST'])
def user_survey_view(request):
    # GET 요청: 저장된 모든 UserSurvey 데이터 조회
    if request.method == 'GET':
        surveys = UserSurvey.objects.all()  # 모든 설문 데이터 가져오기
        serializer = UserSurveySerializer(surveys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST 요청: 새로운 UserSurvey 데이터 생성
    elif request.method == 'POST':
        serializer = UserSurveySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # 데이터 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
