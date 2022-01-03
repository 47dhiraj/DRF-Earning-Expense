from django.urls import path

from .views import GoogleSocialAuthView, FacebookSocialAuthView

urlpatterns = [

    # URL For Google Social Authentication
    path('google/', GoogleSocialAuthView.as_view()),

    # URL for Facebook Social Authentication
    path('facebook/', FacebookSocialAuthView.as_view()),

]
