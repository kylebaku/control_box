from django.contrib import admin
from django.urls import include, path
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('monitoring/', include('monitoring.urls')),
    path('report/', include('report.urls')),
    path('generation/', include('generation.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
