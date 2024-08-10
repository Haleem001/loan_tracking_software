
from datetime import timedelta
from django.db import models, transaction
from django.db.models import F
from django.contrib.auth.models import User
from django.conf import settings
import uuid
from datetime import date
import logging

logger = logging.getLogger(__name__)



class LoanCategory(models.Model):
    """
    Represents a category of loans that can be requested by users.
    
    The `LoanCategory` model defines the following fields:
    
    - `loan_name`: The name of the loan category, with a maximum length of 250 characters.
    - `creation_date`: The date when the loan category was created, automatically set when the object is created.
    - `updated_date`: The datetime when the loan category was last updated, automatically set when the object is saved.
    
    The `__str__` method returns the `loan_name` as the string representation of the object.
    """
        
    loan_name = models.CharField(max_length=250)
    creation_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.loan_name
class FoodItem(models.Model):
    """
    Represents a food item that can be added to a user's cart.
    
    The `FoodItem` model defines the following fields:
    
    - `name`: The name of the food item, with a maximum length of 250 characters.
    - `price`: The price of the food item, represented as a decimal number with up to 10 digits and 2 decimal places.
    
    The `__str__` method returns the `name` as the string representation of the object.
    """
        
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # slug = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.name
class CartItem(models.Model):
    """
    Represents a cart item that a user has added to their cart.
    
    The `CartItem` model defines the following fields:
    
    - `user`: A foreign key to the `CustomUser` model, representing the user who added the item to their cart.
    - `food_item`: A foreign key to the `FoodItem` model, representing the food item that was added to the cart.
    - `quantity`: The quantity of the food item that was added to the cart, represented as a positive integer.
    - `total_price`: The total price of the cart item, calculated as the price of the food item multiplied by the quantity.
    - `creation_date`: The date when the cart item was added to the cart, automatically set when the object is created.
    - `updated_date`: The datetime when the cart item was last updated, automatically set when the object is saved.
    
    The `save` method calculates the `total_price` of the cart item based on the `quantity` and the `price` of the `FoodItem`.
    
    The `__str__` method returns a string representation of the cart item, showing the quantity and the name of the food item.
    
    The `get_total_price` method returns the total price of the cart item.
    """
        

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_user')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_price = self.food_item.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} of {self.food_item.name}"
    
    def get_total_price(self):
        return self.quantity * self.food_item.price


class LoanRequest(models.Model):
    """
    Represents a loan request made by a user.
    
    The `LoanRequest` model defines the following fields:
    
    - `user`: A foreign key to the `CustomUser` model, representing the user who made the loan request.
    - `total_amount`: The total amount of the loan request, represented as a decimal value.
    - `creation_date`: The date and time when the loan request was created, automatically set when the object is created.
    - `status`: The status of the loan request, which can be 'PENDING', 'APPROVED', or 'REJECTED'. The default status is 'PENDING'.
    - `cart_items`: A many-to-many relationship with the `CartItem` model, representing the items in the user's cart that are part of the loan request.
    - `requested`: A boolean field indicating whether the loan request has been submitted.
    - `status_date`: The date and time when the loan request status was last updated.
    - `repayment_date`: The date when the loan should be repaid.
    - `payable_loan`: The amount of the loan that is still payable.
    - `payment_status`: The status of the loan payment, which can be 'PENDING', 'PAID', or 'UNPAID'. The default status is 'PENDING'.
    
    The `save` method calculates the `payable_loan` based on the `total_amount` field.
    
    The `__str__` method returns a string representation of the loan request, showing the username of the user and the total amount.
    
    The `calculate_total_amount` method calculates the total amount of the loan request by summing the total prices of the items in the user's cart.
    
    The `approve` method approves the loan request by creating or updating a `Loan` object for the user and updating the status of the loan request.
    
    The `reject` method rejects the loan request by updating the status of the loan request.
    """
    reference_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loan_requests_user')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    creation_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    ], default='PENDING')

    cart_items = models.ManyToManyField(CartItem)
    requested = models.BooleanField(default=False)
    
    status_date = models.DateField(null=True, blank=True, default=None)
    repayment_date = models.DateField(null=True, blank=True, default=None)
    payable_loan = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('UNPAID', 'Unpaid')
    ], default='PENDING')

    def save(self, *args, **kwargs):
        if  self.total_amount:
            self.payable_loan = self.total_amount  
        
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Loan Request for {self.user.username} - {self.total_amount}"

    def calculate_total_amount(self):
        return sum(item.cart_item.get_total_price() for item in self.cart_items.all())

    def approve(self):
       

        # repayment_period = (self.repayment_date - self.creation_date.date()).days / 365
        loan, created = Loan.objects.get_or_create(user=self.user)
        if not created:
            if loan.total_loan and loan.payable_loan is not None:
                loan.total_loan += self.total_amount
                loan.payable_loan += self.total_amount 
            else:
                loan.total_loan = self.total_amount
                loan.payable_loan = self.total_amount
        else:
            loan.total_loan = self.total_amount
            loan.payable_loan = self.total_amount
        
        loan.save()
        
        today = date.today()
        self.status_date = today
        self.status = 'APPROVED'
        self.save()

    def reject(self):
        today = date.today()
        self.status_date = today
        self.status = 'REJECTED'
        self.save()



class Loan(models.Model):
    """
    Represents a loan associated with a user.
    
    The `Loan` model has the following fields:
    
    - `user`: A foreign key to the `CustomUser` model, representing the user associated with the loan.
    - `total_loan`: A positive integer field representing the total loan amount.
    - `payable_loan`: A positive integer field representing the remaining payable loan amount.
    
    The `__str__` method returns the username of the associated user.
    
    The `make_payment` method creates a new `LoanTransaction` object with the provided payment amount, updates the `payable_loan` field, and returns the created transaction.
    """
        
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_loan')
    total_loan = models.PositiveIntegerField(default=0)
    payable_loan = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username
    def make_payment(self, amount):
        transaction = LoanTransaction.objects.create(
            loan=self,
            user=self.user,
            amount=amount
        )
        return transaction


class LoanTransaction(models.Model):
    """
    Represents a loan transaction associated with a user and a loan.
    
    The `LoanTransaction` model has the following fields:
    
    - `user`: A foreign key to the `CustomUser` model, representing the user associated with the transaction.
    - `loan`: A foreign key to the `Loan` model, representing the loan associated with the transaction.
    - `transaction`: A UUID field that serves as the primary key for the transaction.
    - `payment`: A positive integer field representing the payment amount.
    - `payment_date`: A date field representing the date of the payment, automatically set to the current date when the transaction is created.
    
    The `__str__` method returns the username of the associated user.
    
    The `save` method performs an atomic transaction to update the `payable_loan` field of the associated loan by subtracting the payment amount. If the payment amount exceeds the payable loan amount, a `ValueError` is raised.
    """
    transaction_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transaction_user')
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='transactions')
    
    amount = models.PositiveIntegerField(default=0)
    payment_date = models.DateField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('UNPAID', 'Unpaid')
    ], default='PENDING')

    def __str__(self):
        return self.user.username
    def save(self, *args, **kwargs):

        self.loan.payable_loan = F('payable_loan') - self.amount
        self.loan.save()  
        logger.info(f"Loan payment of {self.amount} processed for loan {self.loan.id}")
        super().save(*args, **kwargs)

    
    



class LoanRequestItem(models.Model):
    loan_request = models.ForeignKey(LoanRequest, on_delete=models.CASCADE, related_name='loan_items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} of {self.food_item.name} for {self.loan_request}"



