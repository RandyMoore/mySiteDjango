from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^images/$', views.ImageList.as_view()),
    url(r'^images/(?P<pk>[0-9]+)$', views.ImageDetail.as_view()),
]