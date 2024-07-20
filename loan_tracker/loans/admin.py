from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from django.http import HttpResponseRedirect
from .models import   Loan, LoanTransaction , FoodItem, LoanRequest, CartItem

# Register your models here.



class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'food_item', 'quantity','total_price']
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
class LoanTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment', 'payment_date']
class LoanAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_loan', 'payable_loan']
class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_amount', 'status', 'creation_date', 'repayment_date', 'approve_button', 'reject_button']
    
    list_filter = ['status']
    def approve_button(self, obj):
        url = reverse('admin:approve_loan', args=[obj.pk])
        return format_html('<a href="{}" class="btn btn-success">Approve</a>', url)

    def reject_button(self, obj):
        url = reverse('admin:reject_loan', args=[obj.pk])
        return format_html('<a href="{}" class="btn btn-danger">Reject</a>', url)
    
    approve_button.short_description = 'Approve'
    approve_button.allow_tags = True

    reject_button.short_description = 'Reject'
    reject_button.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('approve/<int:item_id>/', self.admin_site.admin_view(self.approve_loan), name='approve_loan'),
            path('reject/<int:item_id>/', self.admin_site.admin_view(self.reject_loan), name='reject_loan'),
        ]
        return custom_urls + urls

    def approve_loan(self, request, item_id):
        item = self.get_object(request, item_id)
        item.approve()  # Call the approve method on the model instance
        self.message_user(request, "Item approved successfully.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def reject_loan(self, request, item_id):
        item = self.get_object(request, item_id)
        item.reject()  # Call the reject method on the model instance
        self.message_user(request, "Item rejected successfully.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    


    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        # Additional actions after saving related objects
        loan_request = form.instance

        # Update total_amount or perform other actions if needed
        loan_request.total_amount = loan_request.calculate_total_amount()
        loan_request.save()
   
admin.site.register(LoanRequest, LoanRequestAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(LoanTransaction, LoanTransactionAdmin)
admin.site.register(FoodItem,FoodItemAdmin)
admin.site.register(CartItem, CartItemAdmin)