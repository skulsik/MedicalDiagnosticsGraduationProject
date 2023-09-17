from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import TemplateView

from users.apps import UsersConfig
from users.forms import UserLoginForm
from users.views import RegisterView, UserActivate, InvalidUserActivate, UserPasswordResetView, \
    UserPasswordResetDoneView, ProfileView, ProfileUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html', authentication_form=UserLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm_email/', TemplateView.as_view(template_name='users/confirm_email.html'), name='confirm_email'),
    path('verify_email/<uidb64>/<token>/', UserActivate.as_view(), name='verify_email'),
    path('user_activate', TemplateView.as_view(template_name='users/user_activate.html'), name='user_activate'),
    path('invalid_user_activate/', InvalidUserActivate.as_view(), name='invalid_user_activate'),
    path('reset_password/', UserPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update', ProfileUpdateView.as_view(), name='profile_update'),
]
