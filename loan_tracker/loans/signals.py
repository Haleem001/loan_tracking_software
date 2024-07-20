
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LoanRequest
from .utils import send_rejection_email,send_approval_email

@receiver(post_save, sender=LoanRequest)
def handle_adoption_request_status_change(sender, instance, created, **kwargs):
    if not created:
        if instance.status == 'APPROVED':
            send_approval_email(instance)
        elif instance.status == 'REJECTED':
            send_rejection_email(instance)