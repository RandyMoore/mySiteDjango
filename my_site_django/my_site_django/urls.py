from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from weblog import urls as weblog_urls

urlpatterns = ([] if settings.PRODUCTION else [url(r'^admin/', admin.site.urls)]) + [
    url(r'^audits/', include('government_audit.urls')),
    url(r'', include(weblog_urls)),
]