from django.urls import path
from .views import user_login, logout_view, dashboard_view, CustomPasswordChangeView, register_user
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard_user'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('register/', register_user, name='register_user'),
]
