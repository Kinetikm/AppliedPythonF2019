from django.urls import path

from .views import CreateUserAPIView, ObtainTokenAPIView

app_name = "users"

urlpatterns = [
    path('registration/', CreateUserAPIView.as_view()),
    path('obtain-token/', ObtainTokenAPIView.as_view()),
]

