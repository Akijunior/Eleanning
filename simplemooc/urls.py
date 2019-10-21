from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from simplemooc.routers import router

urlpatterns = [
    url(r'^', include(('simplemooc.core.urls','core'), namespace='core')),
    url(r'^conta/', include(('simplemooc.accounts.urls','accounts'), namespace='accounts')),
    url(r'^cursos/', include(('simplemooc.courses.urls', 'courses'), namespace='courses')),
    url(r'^admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
