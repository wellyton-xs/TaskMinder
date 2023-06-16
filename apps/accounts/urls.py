from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = "accounts"

urlpatterns = [
    path('add_user/', views.add_user, name="add_user"),
    #path('login/', views.login_user, name="login"),
    path('logout_user/', views.logout_user, name="logout"),
    path('change_password/', views.change_password, name="change_password"),
    path('profile/', views.view_profile, name="user_profile"),
    path('change_profile/', views.change_user_profile, name="change_profile"),
    path('more_info/', views.more_info, name="+info"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='tasks/accounts/reset_pass.html'), name='recovery'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='tasks/accounts/reset_pass_done.html'), name='password_reset_done'),
    path('password-reset/confirm/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(template_name='tasks/accounts/reset_pass_confirm.html'), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='tasks/accounts/reset_pass_complete.html'), name='password_reset_complete'),
]