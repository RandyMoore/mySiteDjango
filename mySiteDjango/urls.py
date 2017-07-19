from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    url(r'^$', include('home.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^weblog/', include('weblog.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
