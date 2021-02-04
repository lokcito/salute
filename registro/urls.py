from django.urls import include, path, re_path
from django.conf import settings
from registro import views

urlpatterns = [
	re_path('^reportes/$', views.reports),
]