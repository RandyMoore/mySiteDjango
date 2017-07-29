from django.conf.urls import url, include
from django.conf.urls.static import static

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls

from my_site_django import settings


urlpatterns = [
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'', include(wagtail_urls)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)