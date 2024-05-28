from django.urls import path
from .views import home_page, about_page, courses_view, contact_me_view, playlists_view


urlpatterns = [
    path('', home_page, name='home_page'),
    path('about/', about_page, name='about_page'),
    path('courses/', courses_view, name='courses_view'),
    path('contact-me/', contact_me_view, name='contact_me'),
    path('playlists/', playlists_view, name='playlists_view'),
]
