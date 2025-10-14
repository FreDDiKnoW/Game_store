from django.urls import path
from .views import UserRegistrationView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Refresh
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), # Verify
]