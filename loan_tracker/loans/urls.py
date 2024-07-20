from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .views import  UserDashboardAPI,  LoanRequestAPI, LoanPaymentAPI, UserTransactionAPI, UserLoanHistoryAPI

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'food-items', views.FoodItemViewSet)
router.register(r'loan-requests', views.LoanRequestViewSet, basename='loanrequest')

schema_view = get_schema_view(
   openapi.Info(
      title="Loan Tracker API",
      default_version='v1',
      description="API documentation for the Adoption App",
      terms_of_service="https://www.yourapp.com/terms/",
      contact=openapi.Contact(email="contact@yourapp.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('user-dashboard/', UserDashboardAPI.as_view(), name='user-dashboard-api'),
    path('loan-request/', LoanRequestAPI.as_view(), name='api-loan-request'),
    path('loan-payment/', LoanPaymentAPI.as_view(), name='api-loan-payment'),
    path('user-transactions/', UserTransactionAPI.as_view(), name='api-user-transactions'),
    path('user-loan-history/', UserLoanHistoryAPI.as_view(), name='api-user-loan-history'),
    path('', include(router.urls)),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('view-cart/', views.view_cart, name='view-cart'),
    path('checkout/', views.checkout, name='checkout'),
    
]







