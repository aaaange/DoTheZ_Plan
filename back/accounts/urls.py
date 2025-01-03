from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('api/v1/login/', views.login, name='login'),  # 로그인 API
    path('api/v1/logout/', views.logout, name='logout'),  # 로그아웃 API
    path('api/v1/signup/', views.signup, name='signup'),  # 회원가입 API
    path('api/v1/delete/', views.delete, name='delete'),  # 계정 삭제 API
    path('api/v1/update/', views.update, name='update'),  # 사용자 정보 수정 API
    path('api/v1/change_password/', views.change_password, name='change_password'),  # 비밀번호 변경 API
    path('api/v1/check_username/', views.check_username, name = 'check_username'),      # 아이디 중복 체크
    path('api/v1/profile/<int:user_id>/', views.profile, name='profile'),  # 프로필 페이지 API
    path('api/v1/profile/<int:user_id>/reviews/count/', views.user_review_count, name="user_review_count"),
    path('api/v1/subscribe/<str:fin_prdt_cd>/', views.toggle_product_subscription, name='toggle_product_subscription'),  # 상품 가입 토글하기
    path('api/v1/check_state/<str:fin_prdt_cd>/', views.check_state, name='check_state'),     # 구독 상태 확인
    path('api/v1/my/', views.my_subscribed_products, name='my_subscribed_products'),  # 내가 가입한 상품 목록을 반환
    path('api/v1/user_info/', views.user_info, name='user_info'),     # 로그인 인증 구현
]