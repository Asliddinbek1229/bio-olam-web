from django.urls import path
from .views import user_login, logout_view


urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
]
