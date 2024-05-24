from django.urls import path
from .views import user_login, logout_view, dashboard_view, CustomPasswordChangeView, register_user, edit_user_profile, add_teacher, \
      teachers_view, teacher_profiles_view
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard_user'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('register/', register_user, name='register_user'),
    path('update-profile/', edit_user_profile, name='edit_user_profile'),
    path('add-teacher/', add_teacher, name='add_teacher'),
    path('teachers/', teachers_view, name='teachers_view'),
    path('teacher-profile/<int:id>/', teacher_profiles_view, name='teacher_profile'),
]
