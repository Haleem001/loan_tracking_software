from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from django.apps import apps


class CustomUserManager(UserManager):
    def create_user(self,Status, username, email, password , first_name, last_name):
        if not Status:
            raise ValueError("User must be a staff or admin user")
        if not username:
            raise ValueError("User must have a username")
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            return ValueError("User must have a last name")

        email = self.normalize_email(email)
        user = self.model(
            Status=Status,
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name

        )
        user.is_admin = False
        user.is_staff = False
        user.is_superuser = False
        user.is_anonymous = False
        user.save(using=self._db)
        return user

    def create_superuser(self, Status, username, email,  password, first_name, last_name):
        if not Status:
            raise ValueError("User must be a staff or admin user")
        if not username:
            raise ValueError("User must have a username")
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            return ValueError("User must have a last name")
        

        email = self.normalize_email(email)
        user = self.model(
            Status=Status,
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name

        )
        user.set_password(password)  # change password to hash
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_anonymous = False
        user.save(using=self._db)
        return user

    def create_staffuser(self, Status, username,  email,  password, first_name , last_name):
        if not Status:
            raise ValueError("User must be a staff or admin user")
        if not username:
            raise ValueError("User must have a username")
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            return ValueError("User must have a last name")

        email = self.normalize_email(email)
        user = self.model(
            Status=Status,
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name

        )
        user.set_password(password)  # change password to hash
        user.is_admin = False
        user.is_staff = True
        user.is_superuser = False
        user.is_anonymous = False
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    ADMIN = "Admin"
    STAFF = "Staff"
    USER = "User"
    STATUS_CHOICES = [
        (ADMIN, ("Admin")),
        (STAFF, ("Staff")),
        (USER, ("User")),
    ]
    Status = models.CharField(choices=STATUS_CHOICES,
                              max_length=255, default='User')

    username = models.CharField(('username'), unique=True, max_length=255)
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(('first_name'), max_length=255 )
    last_name = models.CharField(('last_name') , max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    @ staticmethod
    def has_perm(perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    @ staticmethod
    def has_module_perms(app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return "{}".format(self.first_name + ' ' + self.last_name)
    
    def generate_report(self):
        Loan = apps.get_model('loans', 'Loan')
        LoanRequest = apps.get_model('loans', 'LoanRequest')
        LoanTransaction = apps.get_model('loans', 'LoanTransaction')

        loans = Loan.objects.filter(user=self)
        loan_requests = LoanRequest.objects.filter(user=self)
        loan_transactions = LoanTransaction.objects.filter(user=self)

        return {
            'username': self.username,
            'loans': [{'total_loan': loan.total_loan, 'payable_loan': loan.payable_loan} for loan in loans],
            'loan_requests': [{'total_amount': req.total_amount, 'status': req.status, 'creation_date': req.creation_date} for req in loan_requests],
            'loan_transactions': [{'payment': trans.payment, 'payment_date': trans.payment_date} for trans in loan_transactions]
        }