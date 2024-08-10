from django.shortcuts import render 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from .models import Loan, LoanTransaction, LoanRequest, CartItem
from .serializers import UserDashboardSerializer, LoanRequestSerializer, LoanTransactionSerializer, GetLoanRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from drf_yasg import openapi
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FoodItem, CartItem, LoanRequest, LoanRequestItem
from .serializers import FoodItemSerializer, CartItemSerializer, LoanHistorySerializer
from django.contrib import messages
from django.http import HttpResponse
import csv
from users.models import CustomUser


class UserDashboardAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requestLoan = LoanRequest.objects.filter(user=request.user).count()
        approved = LoanRequest.objects.filter(user=request.user, status='APPROVED').count()
        rejected = LoanRequest.objects.filter(user=request.user, status='REJECTED').count()
        totalLoan = Loan.objects.filter(user=request.user).aggregate(Sum('total_loan'))['total_loan__sum'] or 0
        currentLoan = Loan.objects.filter(user=request.user).aggregate(Sum('payable_loan'))['payable_loan__sum'] or 0
        paidLoan = totalLoan - currentLoan
        totalPaid = LoanTransaction.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0

        data = {
            'request': requestLoan,
            'approved': approved,
            'rejected': rejected,
            'total_loan': totalLoan,
            'current_loan': currentLoan,
            'paid_loan': paidLoan,
            'total_paid': totalPaid,
        }

        serializer = UserDashboardSerializer(data)
        return Response(serializer.data)

    
class LoanRequestAPI(APIView):
    """
    API endpoint for handling loan requests.
    
    This API endpoint allows authenticated users to create new loan requests and retrieve their existing loan requests.
    
    The `LoanRequestAPI` class provides the following functionality:
    
    - `POST /loan-requests/`: Create a new loan request. The request body should contain the required fields (reason, amount, category, year) in the expected format.
    - `GET /loan-requests/`: Retrieve all loan requests for the authenticated user.
    
    The API uses the `LoanRequestSerializer` to serialize the loan request data, and provides detailed error messages in case of invalid requests.
    """
        
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Create a new loan request",
        request_body=LoanRequestSerializer,
        responses={
            201: LoanRequestSerializer,
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": {
                            "field": ["error message"]
                        },
                        "required_format": {
                            "reason": "string",
                            "amount": "number",
                            "category": "string",
                            "year": "integer"
                        }
                    }
                }
            )
        }
    )

    def post(self, request):
        serializer = LoanRequestSerializer(data=request.data)
        if serializer.is_valid():
            loan_request = serializer.save(user = request.user)
            return Response(LoanRequestSerializer(loan_request).data, status=status.HTTP_201_CREATED)
        return Response({
            'error': serializer.errors,
            'required_format': {
                "reason": "string",
                "amount": "number",
                "category": "string",
                "year": "integer"
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Get all loan requests for the authenticated user",
        responses={200: LoanRequestSerializer(many=True)}
    )
    def get(self, request):
        loan_requests = LoanRequest.objects.filter(user=request.user)
        serializer = GetLoanRequestSerializer(loan_requests, many=True)
        return Response(serializer.data)

   
class LoanPaymentAPI(APIView):
    """
    Provides an API endpoint for managing loan payments for authenticated users.
    
    The `LoanPaymentAPI` class is an `APIView` that handles GET and POST requests related to loan payments.
    
    GET requests:
    - Retrieves all loan transactions for the authenticated user.
    - Returns a list of `LoanTransactionSerializer` objects.
    
    POST requests:
    - Processes a new loan payment for the authenticated user.
    - Validates the payment amount using the `LoanTransactionSerializer`.
    - Updates the user's loan balance by calling the `make_payment` method on the user's `Loan` object.
    - Returns a success message and the transaction ID.
    """
        
    permission_classes = [IsAuthenticated]
    

    def get(self, request):
        payments = LoanTransaction.objects.filter(user=request.user)
        serializer = LoanTransactionSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LoanTransactionSerializer(data=request.data)
        if serializer.is_valid():
            amount = request.data.get('amount')
            try:
                loan = Loan.objects.get(user=request.user)
                transaction = loan.make_payment(amount)
                serializer.save(user=request.user, loan=loan, amount=amount)
                return Response({"message": "Payment successful", "transaction_id": str(transaction.transaction_id)}, status=status.HTTP_200_OK)
            except Loan.DoesNotExist:
                return Response({"error": "No active loan found for this user"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

    


    
    
class UserTransactionAPI(APIView):
    """
    Provides an API endpoint for retrieving all loan transactions for the authenticated user.
    
    The `UserTransactionAPI` class is an `APIView` that handles GET requests to retrieve the user's loan transactions.
    
    GET requests:
    - Retrieves all loan transactions for the authenticated user.
    - Returns a list of `LoanTransactionSerializer` objects.
    """
        
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = LoanTransaction.objects.filter(user=request.user)
        serializer = LoanTransactionSerializer(transactions, many=True)
        return Response(serializer.data)

class UserLoanHistoryAPI(APIView):
    """
    Provides an API endpoint for retrieving all loan requests for the authenticated user.
    
    The `UserLoanHistoryAPI` class is an `APIView` that handles GET requests to retrieve the user's loan requests.
    
    GET requests:
    - Retrieves all loan requests for the authenticated user.
    - Returns a list of `LoanRequestSerializer` objects.
    """
        
    permission_classes = [IsAuthenticated]

    def get(self, request):
        loans = LoanRequest.objects.filter(user=request.user)
        serializer = LoanRequestSerializer(loans, many=True)
        return Response(serializer.data)
class FoodItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    The `FoodItemViewSet` class is a `ReadOnlyModelViewSet` that provides a read-only API for accessing `FoodItem` objects.
    
    The `queryset` attribute specifies that all `FoodItem` objects should be returned.
    
    The `serializer_class` attribute specifies that the `FoodItemSerializer` should be used to serialize the `FoodItem` objects.
    """
        
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer

@api_view(['POST'])
def add_to_cart(request):
    """
    Adds a food item to the user's cart. If the user already has an existing loan request with an open cart, the item is added to that cart. Otherwise, a new loan request is created with the item in the cart.
    
    Args:
        request (django.http.request.HttpRequest): The HTTP request object.
    
    Returns:
        django.http.response.Response: A response indicating that the item was added to the cart.
    """
        
    food_item_id = request.data.get('food_item_id')
    quantity = request.data.get('quantity', 1)

    try:
        food_item = FoodItem.objects.get(id=food_item_id)
    except FoodItem.DoesNotExist:
        return Response({'error': 'Food item not found'}, status=status.HTTP_404_NOT_FOUND)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        food_item=food_item,
        defaults={'quantity': quantity}
    )
    loan_qs = LoanRequest.objects.filter(user=request.user, requested = False)

    if loan_qs.exists():
        loan_req = loan_qs[0]
        if loan_req.cart_items.filter(food_item__pk=food_item.pk).exists():
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request, "Added quantity Item")
        else:
            loan_req.cart_items.add(cart_item)
            messages.info(request, "Item added to your cart")
    else:
       
        order = LoanRequest.objects.create(user=request.user)
        order.cart_items.add(cart_item)
        messages.info(request, "Item added to your cart")
            


        
   

    return Response({'message': 'Item added to cart'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def view_cart(request):
    """
    Retrieves the cart items for the authenticated user and returns them as a serialized response.
    
    Args:
        request (django.http.request.HttpRequest): The HTTP request object.
    
    Returns:
        django.http.response.Response: A response containing the serialized cart items.
    """
        
    cart_items = CartItem.objects.filter(user=request.user)
    serializer = CartItemSerializer(cart_items, many=True)
    return Response(serializer.data)
import logging

logger = logging.getLogger(__name__)
@api_view(['POST'])
def checkout(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        repayment_date = request.data.get('repayment_date')
        if not repayment_date:
            return Response({'error': 'Repayment date is required'}, status=status.HTTP_400_BAD_REQUEST)

        loan_request = LoanRequest.objects.get(user=request.user, requested=False)
        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        loan_request.total_amount = sum(item.total_price for item in cart_items)
        loan_request.requested = True
        loan_request.repayment_date = repayment_date
        loan_request.save()

        # Create LoanRequestItem instances instead of deleting cart items
        for cart_item in cart_items:
            LoanRequestItem.objects.create(
                loan_request=loan_request,
                food_item=cart_item.food_item,
                quantity=cart_item.quantity,
                price=cart_item.total_price
            )

        # Clear the user's cart
        cart_items.delete()

        
        serializer = LoanHistorySerializer(loan_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Error during checkout: {str(e)}")
        return Response({'error': 'An error occurred during checkout'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoanRequestViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LoanRequestSerializer

    def get_queryset(self):
        return LoanRequest.objects.filter(user=self.request.user)

 


class LoanHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        loan_requests = LoanRequest.objects.filter(user=request.user, requested=True)
        serializer = LoanHistorySerializer(loan_requests, many=True)
        return Response(serializer.data)



