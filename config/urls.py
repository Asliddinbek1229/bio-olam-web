from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import questions

urlpatterns = [
    path("bio-olam-admin/", admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include("pages.urls")),
    path('accounts/', include("users.urls")),
    path('courses/', include("courses.urls")),
    # path('quiz-app/', include("quiz_app.urls")),
    path('new-quiz/', include('questions.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    # path('admin/', admin.site.urls),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)