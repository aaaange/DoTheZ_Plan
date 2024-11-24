from django.contrib import admin
from django.urls import path, include
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<int:user_pk>/password/', views.change_password, name='change_password'),
    path('accounts/', include('accounts.urls')),
    path('product/', include('product.urls')),
    path('surveys/', include('surveys.urls')),
    path('exchange/', include('exchange.urls')),
]
