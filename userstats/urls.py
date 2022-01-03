from .views import ExpenseSummaryStats, IncomeSourcesSummaryStats

from django.urls import path

urlpatterns = [

    # Url for Expense summary category wise
    path('expenses_cateogry_data/', ExpenseSummaryStats.as_view(), name="expense_category_summary"),

    # Url for Income summary sources wise
    path('income_sources_data/', IncomeSourcesSummaryStats.as_view(), name="income_sources_summary"),

];

