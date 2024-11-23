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
    path('api/v1/subscribe/<str:fin_prdt_cd>/', views.toggle_product_subscription, name='toggle_product_subscription'),  # 상품 가입 토글하기
    path('api/v1/my/', views.my_subscribed_products, name='my_subscribed_products'),  # 내가 가입한 상품 목록을 반환
    path('api/v1/user_info/', views.user_info, name='user_info'),     # 로그인 인증 구현
    path('api/v1/product_graph/', views.subscribed_products_graph, name="subscribed_products_graph")  # 상품 금리 그래프 출력
]