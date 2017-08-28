from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.AuditDocumentList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.AuditDocument.as_view()),
]