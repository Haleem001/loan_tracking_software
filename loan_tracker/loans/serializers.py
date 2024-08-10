from rest_framework import serializers
from .models import LoanRequest , LoanTransaction, CartItem, LoanRequestItem, FoodItem
from django.conf import settings
from django.apps import apps


class UserDashboardSerializer(serializers.Serializer):
    request = serializers.IntegerField()
    approved = serializers.IntegerField()
    rejected = serializers.IntegerField()
    total_loan = serializers.DecimalField(max_digits=10, decimal_places=2)

    paid_loan = serializers.DecimalField(max_digits=10, decimal_places=2)
    current_loan = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_paid = serializers.DecimalField(max_digits=10, decimal_places=2)


    

# class LoanRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LoanRequest
#         fields = ['id',  'total_amount', 'repayment_date', 'user']

class LoanTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanTransaction
        fields = ['transaction_id','amount', 'payment_date','user']

class GetLoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = ['id',  'total_amount',  'repayment_date', 'user', 'status']







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
        fields = ['id', 'user',  'total_amount', 'creation_date', 'repayment_date', 'payable_loan', 'payment_status', 'status']
        read_only_fields = ['user', 'total_amount', 'payable_loan', 'payment_status']

    
class LoanRequestItemSerializer(serializers.ModelSerializer):
    food_item_name = serializers.CharField(source='food_item.name')
    
    class Meta:
        model = LoanRequestItem
        fields = ['food_item_name', 'quantity', 'price']

class LoanHistorySerializer(serializers.ModelSerializer):
    loan_items = LoanRequestItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = LoanRequest
        fields = ['id', 'total_amount', 'creation_date', 'status', 'loan_items', 'status', 'repayment_date', 'reference_number']
