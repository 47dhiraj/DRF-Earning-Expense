from rest_framework import serializers
from .models import Expense


class ExpensesSerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length=1024, min_length=1)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Expense
        fields = ['id', 'date', 'description', 'amount', 'category']


