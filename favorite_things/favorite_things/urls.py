from django.conf.urls import url, include
from django.contrib import admin

# Wire up our API using automatic URL routing.

urlpatterns = [

    # admin
    url(r'^admin/', admin.site.urls),

    # API
    url(r'^api/', include('main.url', namespace="main",)),

    url('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
