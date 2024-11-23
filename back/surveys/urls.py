from django.urls import path
from . import views

appname="surveys"
urlpatterns = [
    path('user-survey/<int:user>/', views.user_survey_view, name='user-survey'),
    path('product-filtering/<int:user_survey_id>/', views.recommend_product, name='recommend_product'),
]
