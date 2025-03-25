from django.urls import path, include
from accounts.views import *
from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns = [
    path('login',login_view,name='login'),
    path('logout',logout_view,name='logout'),
    path('signup',signup_view,name='signup'),
    # path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
    # path('forgot-password/',forgot_password_view, name='forgot_password'),
    # path('reset-password/',reset_password_view, name='reset_password'),
    # path('password-reset-complete/',password_reset_complete_view, name='password_reset_complete'),

