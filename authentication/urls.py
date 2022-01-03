from django.urls import path
from .views import RegisterView, VerifyEmail, LoginAPIView, LogoutAPIView, RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPasswordAPIView

from rest_framework_simplejwt.views import (TokenRefreshView, )


urlpatterns = [

    # URL for Registration
    path('register/', RegisterView.as_view(), name="register"),

    # URL for verifying user registration by clicking email
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),

    # URL for logging the user
    path('login/', LoginAPIView.as_view(), name="login"),

    # URL for Refreshing the token  (rest_framework_simplejwt le nai diyeko url ho)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # URL for logging out the user
    path('logout/', LogoutAPIView.as_view(), name="logout"),

    # The below three url are for resetting the user password by email
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(), name='password-reset-complete')

]
