from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import RegisterUserSerializer, ChangePasswordSerializer, UserSerializer
import csv
from django.http import HttpResponse

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
                row.extend([trans['payment'], trans['payment_date']])
            else:
                row.extend(['', ''])

            writer.writerow(row)

    return response