from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView)
from .views import (
    MyTokenObtainPairView, ChangePasswordView , RegisterUser, UserList, UserDetail, ForgotPasswordView, ResetPasswordView)

urlpatterns = [
    path('authtoken/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('register/', RegisterUser.as_view(), name="register"),
    path('users/', UserList.as_view() , name='user_list_view'),
    path('users/<int:pk>', UserDetail.as_view()),
    path('changepassword/<int:pk>',
         ChangePasswordView.as_view(), name='change_password'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),

]