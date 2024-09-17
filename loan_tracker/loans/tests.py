from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import LoanCategory, FoodItem, CartItem, LoanRequest, Loan, LoanTransaction, LoanRequestItem
from decimal import Decimal
from datetime import date

User = get_user_model()

class LoanCategoryModelTest(TestCase):
    def setUp(self):
        self.loan_category = LoanCategory.objects.create(loan_name="Test Loan Category")

    def test_loan_category_creation(self):
        self.assertEqual(self.loan_category.loan_name, "Test Loan Category")
        self.assertIsNotNone(self.loan_category.creation_date)
        self.assertIsNotNone(self.loan_category.updated_date)

class FoodItemModelTest(TestCase):
    def setUp(self):
        self.food_item = FoodItem.objects.create(name="Test Food", price=Decimal('10.99'))

    def test_food_item_creation(self):
        self.assertEqual(self.food_item.name, "Test Food")
        self.assertEqual(self.food_item.price, Decimal('10.99'))

class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            Status='ACTIVE',
            username='testuser',
            email='testuser@example.com',
            password='12345',
            first_name='Test',
            last_name='User'
        )
        self.food_item = FoodItem.objects.create(name="Test Food", price=Decimal('10.99'))
        self.cart_item = CartItem.objects.create(user=self.user, food_item=self.food_item, quantity=2)

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.user, self.user)
        self.assertEqual(self.cart_item.food_item, self.food_item)
        self.assertEqual(self.cart_item.quantity, 2)
        self.assertEqual(self.cart_item.total_price, Decimal('21.98'))

class LoanRequestModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            Status='ACTIVE',
            username='testuser',
            email='testuser@example.com',
            password='12345',
            first_name='Test',
            last_name='User'
        )
        self.loan_request = LoanRequest.objects.create(user=self.user, total_amount=Decimal('100.00'))

    def test_loan_request_creation(self):
        self.assertEqual(self.loan_request.user, self.user)
        self.assertEqual(self.loan_request.total_amount, Decimal('100.00'))
        self.assertEqual(self.loan_request.status, 'PENDING')

    def test_loan_request_approve(self):
        self.loan_request.approve()
        self.assertEqual(self.loan_request.status, 'APPROVED')
        self.assertIsNotNone(self.loan_request.status_date)

    def test_loan_request_reject(self):
        self.loan_request.reject()
        self.assertEqual(self.loan_request.status, 'REJECTED')
        self.assertIsNotNone(self.loan_request.status_date)

class LoanModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            Status='ACTIVE',
            username='testuser',
            email='testuser@example.com',
            password='12345',
            first_name='Test',
            last_name='User'
        )
        self.loan = Loan.objects.create(user=self.user, total_loan=1000, payable_loan=1000)

    def test_loan_creation(self):
        self.assertEqual(self.loan.user, self.user)
        self.assertEqual(self.loan.total_loan, 1000)
        self.assertEqual(self.loan.payable_loan, 1000)

    def test_make_payment(self):
        transaction = self.loan.make_payment(500)
        self.assertEqual(transaction.amount, 500)
        self.assertEqual(transaction.user, self.user)

class LoanTransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            Status='ACTIVE',
            username='testuser',
            email='testuser@example.com',
            password='12345',
            first_name='Test',
            last_name='User'
        )
        self.loan = Loan.objects.create(user=self.user, total_loan=1000, payable_loan=1000)
        self.transaction = LoanTransaction.objects.create(user=self.user, loan=self.loan, amount=500)

    def test_loan_transaction_creation(self):
        self.assertEqual(self.transaction.user, self.user)
        self.assertEqual(self.transaction.loan, self.loan)
        self.assertEqual(self.transaction.amount, 500)
        self.assertEqual(self.transaction.payment_status, 'PENDING')

class LoanRequestItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            Status='ACTIVE',
            username='testuser',
            email='testuser@example.com',
            password='12345',
            first_name='Test',
            last_name='User'
        )
        self.loan_request = LoanRequest.objects.create(user=self.user, total_amount=Decimal('100.00'))
        self.food_item = FoodItem.objects.create(name="Test Food", price=Decimal('10.99'))
        self.loan_request_item = LoanRequestItem.objects.create(
            loan_request=self.loan_request,
            food_item=self.food_item,
            quantity=2,
            price=Decimal('21.98')
        )

    def test_loan_request_item_creation(self):
        self.assertEqual(self.loan_request_item.loan_request, self.loan_request)
        self.assertEqual(self.loan_request_item.food_item, self.food_item)
        self.assertEqual(self.loan_request_item.quantity, 2)
        self.assertEqual(self.loan_request_item.price, Decimal('21.98'))


from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import FoodItem, CartItem, LoanRequest, Loan, LoanTransaction
from decimal import Decimal

User = get_user_model()

class LoanWorkflowIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            Status='ACTIVE',
            username='testuser',
            email='testuser@example.com',
            password='12345',
            first_name='Test',
            last_name='User'
        )
        self.food_item = FoodItem.objects.create(name="Test Food", price=Decimal('10.99'))

    def test_loan_workflow(self):
        # Create a cart item
        cart_item = CartItem.objects.create(user=self.user, food_item=self.food_item, quantity=2)
        self.assertEqual(cart_item.total_price, Decimal('21.98'))

        # Create a loan request
        loan_request = LoanRequest.objects.create(user=self.user, total_amount=Decimal('21.98'))
        loan_request.cart_items.add(cart_item)
        self.assertEqual(loan_request.status, 'PENDING')

        # Approve the loan request
        loan_request.approve()
        self.assertEqual(loan_request.status, 'APPROVED')

        # Check if a loan was created
        loan = Loan.objects.get(user=self.user)
        self.assertEqual(loan.total_loan, 21)
        self.assertEqual(loan.payable_loan, 21)

        # Make a payment
        transaction = loan.make_payment(10)
        self.assertEqual(transaction.amount, 10)
        self.assertEqual(transaction.payment_status, 'PENDING')

        # Refresh the loan object from the database
        loan.refresh_from_db()
        self.assertEqual(loan.payable_loan, 11)

        # Check the user's loan history
        loan_history = LoanRequest.objects.filter(user=self.user)
        self.assertEqual(loan_history.count(), 1)
        self.assertEqual(loan_history.first().status, 'APPROVED')

        # Check the user's transaction history
        transaction_history = LoanTransaction.objects.filter(user=self.user)
        self.assertEqual(transaction_history.count(), 1)
        self.assertEqual(transaction_history.first().amount, 10)
