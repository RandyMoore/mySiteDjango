from django.conf.urls import url, include
from django.contrib import admin

from weblog import urls as weblog_urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include(weblog_urls)),
]
