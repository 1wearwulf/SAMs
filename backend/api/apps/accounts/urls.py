from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # User registration
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Password management
    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/change/', views.ChangePasswordView.as_view(), name='change_password'),
    
    # User profile
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    
    # Optional: UserViewSet endpoints
    path('users/me/', views.UserViewSet.as_view({'get': 'me'}), name='user-me'),
]

app_name = 'accounts'
