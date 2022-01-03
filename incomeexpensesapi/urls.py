from django.contrib import admin
from django.urls import path, include


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="INCOME EXPENSES API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.ourapp.com/policies/terms/",
      contact=openapi.Contact(email="contact@expenses.local"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [

    # URL for inbuilt Admin Panel
    path('admin/', admin.site.urls),



    # URL for authentication app
    path('auth/', include('authentication.urls')),

    # URL for expenses app
    path('expenses/', include('expenses.urls')),

    # URL for income app
    path('income/', include('income.urls')),

    # URL For expense summary
    path('userstats/', include('userstats.urls')),



    # URL For Social OAuth
    path('social_auth/', include(('social_auth.urls', 'social_auth'), namespace="social_auth")),



    # yo talako sabai url haru swagger & redoc ko lagi ho
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/api.json/', schema_view.without_ui(cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
