from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView             
from .models import Expense                                                                     
from .serializers import ExpensesSerializer                                                     
from rest_framework import permissions                                                          

from .permissions import IsOwner                                                                

from .pagination import MyPageNumberPagination

# Create your views here.

class ExpenseListAPIView(ListCreateAPIView):
    serializer_class = ExpensesSerializer                                                       
    queryset = Expense.objects.all()                                                            
    permission_classes = (permissions.IsAuthenticated,)                                         
    pagination_class = MyPageNumberPagination

    def perform_create(self, serializer):                                                       
        return serializer.save(owner=self.request.user)                                         

    def get_queryset(self):                                                                     
        return self.queryset.filter(owner=self.request.user)                                    


class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpensesSerializer                                                       
    permission_classes = (permissions.IsAuthenticated, IsOwner,)                                
    queryset = Expense.objects.all()                                                            
    lookup_field = "id"                                                                        

    def get_queryset(self):                                                                     
        return self.queryset.filter(owner=self.request.user)                                    

