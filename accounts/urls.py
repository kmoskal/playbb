from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html'), name='account-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='account-logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='accounts/change_password.html', success_url='change-password-done'), name='account-change-password'),
    path('change-password/change-password-done', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/change_password_done.html'), name='account-change-password-done'),
]
