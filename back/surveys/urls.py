from django.urls import path
from . import views

app_name="surveys"
urlpatterns = [
    path('api/v1/user-survey/', views.user_survey_view, name='user-survey'),                                         # 설문조사 데이터 저장
    path('api/v1/product-filtering/<str:user_survey_id>/', views.recommend_product, name='recommend_product'),       # 필터링 데이터 조회
    path('api/v1/initialize_model/', views.initialize_model, name='initialize_model'),                               # 군집화 모델 초기화
    path('api/v1/recommend_product_for_user/', views.recommend_product_for_user, name='recommend_product_for_user'), # 군집화 바탕 상품 추천 
    path('api/v1/get_product_by_name/', views.get_product_by_name, name='get_product_by_name'),                      # 추천 상품 이름 로드
]
