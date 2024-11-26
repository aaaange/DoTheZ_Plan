from django.urls import path
from . import views

app_name="exchange"
urlpatterns = [
    path('api/v1/exchange/', views.exchange_rate, name='exchange'),
]