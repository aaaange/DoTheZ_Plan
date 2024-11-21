from django.urls import path
from . import views

appname = 'product'
urlpatterns = [
    # path('fetch-saving-products/', views.fetch_saving_products, name='fetch_saving_products'), # 적금 
    # path('fetch-deposit-products/', views.fetch_deposit_products, name='fetch_deposit_products'), # 예금 # API 호출 및 저장
    path('', views.ProductListView, name='product_list'),  # 데이터 조회
    path('save-deposit-products/', views.save_deposit_products, name='save_deposit_products'),
]
