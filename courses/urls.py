from django.urls import path
from . import views

urlpatterns = [
    path('save-playlist/<int:subcategory_id>/', views.save_playlist_view, name='save_playlist'),
    path('add-subcategry/', views.add_subcategory, name='add_subcategory'),
    path('edit-subcategory/<int:id>/', views.edit_subcategory, name='edit_subcategory'),
    path('delete/<int:id>/', views.delete_subcategory, name='delete_subcategory'),
    path('add-video/', views.add_video, name='add_video'),
    path('edit-video/<int:id>/', views.edit_video, name='edit_video'),
    path('delete-video/<int:id>/', views.delete_video, name='delete_video'),
]
