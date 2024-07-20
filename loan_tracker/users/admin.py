# from django.contrib import admin
# from .models import CustomUser
# from django.contrib.auth.admin import UserAdmin



# # Register your models here.

# admin.site.register(CustomUser, UserAdmin)

from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import path
from .views import generate_user_report
from django.apps import apps
from django.template.response import TemplateResponse




class UserAdmin(BaseUserAdmin):
    actions = ['generate_user_report', 'generate_all_users_report']
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email')}
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
    
        return super().get_form(request, obj, **defaults)
    
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'generate_user_report' not in actions:
            actions['generate_user_report'] = (self.generate_user_report, 'generate_user_report', "Generate report for selected user")
        if 'generate_all_users_report' not in actions:
            actions['generate_all_users_report'] = (self.generate_all_users_report, 'generate_all_users_report', "Generate report for all users")
        return actions
    
    def generate_user_report(self, request, queryset):
            if len(queryset) == 1:
                return HttpResponseRedirect(reverse('admin:generate_user_report', args=[queryset[0].pk]))
            self.message_user(request, "Please select only one user to generate a report.")
    generate_user_report.short_description = "Generate report for selected user"
    
    def generate_all_users_report(self, request, queryset):
            return HttpResponseRedirect(reverse('admin:generate_all_users_report'))
    generate_all_users_report.short_description = "Generate report for all users"

    def analytics_dashboard_view(self, request):
        Loan = apps.get_model('loans', 'Loan')
        LoanRequest = apps.get_model('loans', 'LoanRequest')
        LoanTransaction = apps.get_model('loans', 'LoanTransaction')
        context = self.admin_site.each_context(request)
        context['title'] = "Analytics Dashboard"

    # Get data for charts
        loan_requests = LoanRequest.objects.all()
        context['approved_count'] = loan_requests.filter(status='APPROVED').count()
        context['rejected_count'] = loan_requests.filter(status='REJECTED').count()
        context['pending_count'] = loan_requests.filter(status='PENDING').count()

        transactions = LoanTransaction.objects.order_by('payment_date')
        context['transaction_dates'] = [t.payment_date.strftime('%Y-%m-%d') for t in transactions]
        context['transaction_amounts'] = [float(t.payment) for t in transactions]

        return TemplateResponse(request, "admin/analytics_dashboard.html", context)
    
    def get_urls(self):
            urls = super().get_urls()
            custom_urls = [
                path('generate_user_report/<int:user_id>/', self.admin_site.admin_view(generate_user_report), name='generate_user_report'),
                path('generate_all_users_report/', self.admin_site.admin_view(generate_user_report), name='generate_all_users_report'),
                path('analytics-dashboard/', self.admin_site.admin_view(self.analytics_dashboard_view), name='analytics-dashboard'),
            ]
            return custom_urls + urls
    
    

    

# Register the new User admin
admin.site.register(CustomUser, UserAdmin)
