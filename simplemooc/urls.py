from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^', include(('simplemooc.core.urls','core'), namespace='core')),
    url(r'^conta/', include(('simplemooc.accounts.urls','accounts'), namespace='accounts')),
    url(r'^cursos/', include(('simplemooc.courses.urls', 'courses'), namespace='courses')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
