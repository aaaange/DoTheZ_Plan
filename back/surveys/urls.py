from django.urls import path
from . import views

appname="surveys"
urlpatterns = [
    path('user-survey/', views.user_survey_view, name='user-survey'),
]
