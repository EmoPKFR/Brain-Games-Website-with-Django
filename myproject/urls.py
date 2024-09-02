from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path("admin/", admin.site.urls),
    path("", views.homepage),
    path("about/", views.about),
    path("posts/", include("posts.urls")),
    path("users/", include("users.urls")),
    path("math_games/", include("math_games.urls")),
    path("sequence_memory/", include("sequence_memory.urls")),
    path('number_memory/', include('number_memory.urls')),
    path('typing_test/', include('typing_test.urls')),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)