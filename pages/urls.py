from django.urls import path
from .views import home_page, about_page, courses_view, contact_me_view, playlists_view, watch_video_view, like_video

urlpatterns = [
    path('', home_page, name='home_page'),
    path('about/', about_page, name='about_page'),
    path('courses/', courses_view, name='courses_view'),
    path('contact-me/', contact_me_view, name='contact_me'),
    path('courses/playlists/<int:id>/', playlists_view, name='playlists_view'),
    path('courses/playlists/video/<int:id>/', watch_video_view, name='watch_video'),
    path('courses/playlists/video/<int:id>/like/', like_video, name='like_video'),
]
