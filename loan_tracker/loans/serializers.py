from rest_framework import serializers
from .models import LoanRequest , LoanTransaction, CartItem
from django.conf import settings
from django.apps import apps




class UserDashboardSerializer(serializers.Serializer):

    request = serializers.IntegerField()
    approved = serializers.IntegerField()
    rejected = serializers.IntegerField()
    totalLoan = serializers.DecimalField(max_digits=10, decimal_places=2)
    totalPayable = serializers.DecimalField(max_digits=10, decimal_places=2)
    totalPaid = serializers.DecimalField(max_digits=10, decimal_places=2)
    current_loan = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_loan = serializers.DecimalField(max_digits=10, decimal_places=2)
    

# class LoanRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LoanRequest
#         fields = ['id',  'total_amount', 'repayment_date', 'user']

class LoanTransactionSerializer(serializers.ModelSerializer):
    payment = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        CustomUser = apps.get_model('users', 'CustomUser')
        user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
        model = LoanTransaction
        fields = ['payment', 'payment_date', 'user']

class GetLoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = ['id',  'total_amount',  'repayment_date', 'user', 'status']





from .models import FoodItem, CartItem, LoanRequest

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'price']

class CartItemSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer()

    class Meta:
        model = CartItem
        fields = ['id','food_item', 'quantity', 'total_price']

class LoanRequestSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = LoanRequest
        fields = ['id', 'user',  'total_amount', 'creation_date', 'repayment_date', 'payable_loan', 'payment_status']
        read_only_fields = ['user', 'total_amount', 'payable_loan', 'payment_status']

    
