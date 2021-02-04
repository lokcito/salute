from django.contrib import admin
from django.conf import settings
from django.urls import include, path, re_path
from django.contrib.staticfiles import views
from nacido.views import index
urlpatterns = [
	path('', index),
    path('data/', admin.site.urls),
    path('integracion/', include('registro.urls')),
]
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', views.serve),
    ]