from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions                                                          
from .permissions import IsOwner                                                                
import datetime
from expenses.models import Expense
from income.models import Income
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Sum


# Create your views here.

class ExpenseSummaryStats(APIView):                                             
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get_category(self, expense):
        return expense.category

    def get_amount_for_category(self, expenses, category):
        expenses = expenses.filter(category=category)

        # BEST WAY : Using inbuilt Sum method & ORM aggregate method
        amount = expenses.aggregate(Sum("amount"))
        return amount

        # ALTERNATIVE WAY: using logic way (i.e not using inbuilt ORM aggregate method & python Sum method)
        # amount = 0
        # for expense in expenses:
        #     amount += expense.amount
        # return {'amount': str(amount)}


    def get(self, request):
        todays_date = datetime.date.today()
        ayear_ago = todays_date-datetime.timedelta(days=365)
        expenses = Expense.objects.filter(owner=request.user, date__gte=ayear_ago, date__lte=todays_date)
        categories = list(set(map(self.get_category, expenses)))           
        final = {}                                                         

        for category in categories:
            final[category] = self.get_amount_for_category(expenses, category)

        return Response({'expense_category_wise': final}, status=status.HTTP_200_OK)


class IncomeSourcesSummaryStats(APIView):                                   
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get_source(self, income):
        return income.source

    def get_amount_for_source(self, income, source):
        income = income.filter(source=source)

        # BEST WAY : Using inbuilt Sum method & ORM aggregate method
        amount = income.aggregate(Sum("amount"))
        return amount

        # ALTERNATIVE WAY: using logic way (i.e not using inbuilt ORM aggregate method & python Sum method)
        # amount = 0
        # for i in income:
        #     amount += i.amount
        # return {'amount': str(amount)}


    def get(self, request):
        todays_date = datetime.date.today()
        ayear_ago = todays_date-datetime.timedelta(days=365)
        income = Income.objects.filter(owner=request.user, date__gte=ayear_ago, date__lte=todays_date)
        sources = list(set(map(self.get_source, income)))                   
        final = {}                                                          

        for source in sources:
            final[source] = self.get_amount_for_source(income, source)

        return Response({'income_source_wise': final}, status=status.HTTP_200_OK)