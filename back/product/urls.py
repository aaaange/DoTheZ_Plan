from django.urls import path
from . import views

appname = 'product'
urlpatterns = [
    # path('fetch-saving-products/', views.fetch_saving_products, name='fetch_saving_products'), # 적금 
    # path('fetch-deposit-products/', views.fetch_deposit_products, name='fetch_deposit_products'), # 예금 # API 호출 및 저장
    path('deposit/', views.DepositProductListView, name='product_list'),  # 예금 데이터 조회
    path('saving/', views.SavingProductListView, name='product_list'),  # 적금 데이터 조회
    
    path('deposit/<str:fin_prdt_cd>/', views.ProductDetailView.as_view(), name='product_detail'),  # 상세 조회
    path('saving/<str:fin_prdt_cd>/', views.ProductDetailView.as_view(), name='product_detail'),  # 적금 상세 조회
    
    path('save-deposit-products/', views.save_deposit_products, name='save_deposit_products'),
    path('save-saving-projects/', views.save_saving_products, name='save_saving_products'),
    # path('')
]
