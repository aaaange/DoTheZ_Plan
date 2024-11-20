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
]