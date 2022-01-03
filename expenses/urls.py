from django.urls import path
from . import views


urlpatterns = [
    # URL for listing the espenses
    path('', views.ExpenseListAPIView.as_view(), name="expenses"),

    # URL for detail of the particular expenses
    path('<int:id>', views.ExpenseDetailAPIView.as_view(), name="expense"),

]
