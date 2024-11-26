from django.urls import path
from . import views

app_name = 'chatbots'
urlpatterns = [
    path("api/v1/chatbot/", views.chatbot_response, name="chatbot_response"),
]