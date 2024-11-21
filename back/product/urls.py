from django.urls import path
from . import views

appname = 'product'
urlpatterns = [
    path('fetch-saving-products/', views.fetch_saving_products, name='fetch_saving_products'), # 적금 
    path('fetch-deposit-products/', views.fetch_deposit_products, name='fetch_deposit_products'), # 예금 # API 호출 및 저장
    # path('/', views.ProductListView.as_view(), name='product_list'),  # 저장된 데이터 조회
    # path('/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),  # 상세 데이터 조회
]
