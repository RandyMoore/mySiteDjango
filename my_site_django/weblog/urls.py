from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls


urlpatterns = ([] if settings.PRODUCTION else [url(r'^cms/', include(wagtailadmin_urls))]) + [
    url(r'', include(wagtail_urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)