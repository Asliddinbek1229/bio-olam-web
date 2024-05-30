from django.urls import path
from . import views

urlpatterns = [
    path('save-playlist/<int:subcategory_id>/', views.save_playlist_view, name='save_playlist'),
]
