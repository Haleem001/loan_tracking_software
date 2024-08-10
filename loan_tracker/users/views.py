from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import RegisterUserSerializer, ChangePasswordSerializer, UserSerializer
import csv
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated , AllowAny
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status

import logging

logger = logging.getLogger(__name__)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['id'] = user.id
        token['status'] = user.Status
        token['username'] = user.username
        token['email'] = user.email
        token['first_name']= user.first_name
        token["last_name"]= user.last_name
        

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Takes the username an password an returns access an refresh tokens
    These can be used for user authentication 
    """
    serializer_class = MyTokenObtainPairSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    Used for users to change passwords based on their old password
    """
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated)
    serializer_class = ChangePasswordSerializer


class UserList(generics.ListAPIView):
    """List all users this is only available for an admin user"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    
class RegisterUser(generics.CreateAPIView):
    """This can be used to register new users on the app"""
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """ View , update and delete a specific user's detail"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

def generate_user_report(request, user_id=None):
    if user_id:
        users = [CustomUser.objects.get(id=user_id)]
    else:
        users = CustomUser.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="user_loan_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Total Loans', 'Payable Loans', 'Loan Request Amount', 'Loan Request Status', 'Loan Request Date', 'Loan Transaction Payment', 'Loan Transaction Date'])

    for user in users:
        report_data = user.generate_report()
        total_loans = sum(loan['total_loan'] for loan in report_data['loans'])
        payable_loans = sum(loan['payable_loan'] for loan in report_data['loans'])

        loan_requests = report_data['loan_requests']
        loan_transactions = report_data['loan_transactions']

        max_rows = max(len(loan_requests), len(loan_transactions))

        for i in range(max_rows):
            row = [report_data['username'], total_loans, payable_loans]

            if i < len(loan_requests):
                req = loan_requests[i]
                row.extend([req['total_amount'], req['status'], req['creation_date']])
            else:
                row.extend(['', '', ''])

            if i < len(loan_transactions):
                trans = loan_transactions[i]
                row.extend([trans['amount'], trans['payment_date']])
            else:
                row.extend(['', ''])

            writer.writerow(row)

    return response



class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            token = RefreshToken.for_user(user).access_token
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{str(token)}/"
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email]
            )
            return Response({"message": "Password reset link sent"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        password = request.data.get('password')
        try:
            user = RefreshToken(token).get_user()
            user.set_password(password)
            user.save()
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
        except Exception as e:

            logger.error(f"Error : {str(e)}")

            return Response({"error": "Invalid token or token expired"},status=status.HTTP_400_BAD_REQUEST)