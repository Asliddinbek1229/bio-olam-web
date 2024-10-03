from django.urls import path
from .views import home_page, about_page, courses_view, contact_me_view, playlists_view, watch_video_view, like_video, category_detail_view, \
tutor_contact_view, SearchResultsView, playlist_pay, playlists_done, to_pay, earning_list
from quiz_app.views import quiz_detail_view, quiz_detail_data_view, save_quiz_view

urlpatterns = [
    path('', home_page, name='home_page'),
    path('about/', about_page, name='about_page'),
    path('courses/', courses_view, name='courses_view'),
    path('contact-me/', contact_me_view, name='contact_me'),
    path('tutor-contact/', tutor_contact_view, name='tutor_contact'),
    path('category-detail/<int:id>/', category_detail_view, name='category_detail'),
    path('courses/playlists/<int:id>/', playlists_view, name='playlists_view'),
    path('courses/playlists/<int:id>/pay/', playlists_done, name='playlist_pay'),
    path('courses/playlists/<int:id>/pay/done', playlist_pay, name='playlists_pay'),
    path('courses/playlists/video/<int:id>/', watch_video_view, name='watch_video'),
    path('courses/playlists/quiz/<int:id>/', quiz_detail_view, name='quiz_detail_view'),
    path('courses/playlists/quiz/<int:id>/data', quiz_detail_data_view, name='quiz_data_view'),
    path('courses/playlists/quiz/<int:id>/save', save_quiz_view, name='quiz_save_view'),
    path('courses/playlists/video/<int:id>/like/', like_video, name='like_video'),
    path('search-results/', SearchResultsView.as_view(), name='search_results'),
    path('to-pay-account/', to_pay, name='to_pay'),
    path('earning/', earning_list, name='earning'),
]
