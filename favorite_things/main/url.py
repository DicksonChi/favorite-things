from django.conf.urls import url

from main import views


app_name = "main"

urlpatterns = [
    url(r'^GetCategory/(?P<user>[0-9a-f-]+)/$', views.GetCategory.as_view(), name='get_category'),
    url(r'^Register/$', views.UserCreateView.as_view(), name='add_user'),
    url(r'^Find/(?P<email>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',
        views.UserRetrieveView.as_view(),
        name='find_user'),
    url(r'^GetLog/(?P<user_id>[0-9a-f-]+)/$', views.GetUserLog.as_view(), name='get_user_log'),
    url(r'^CategoryCreate/$', views.CategoryCreateView.as_view(), name='create_category'),
    url(r'^CreateThing/$', views.FavThingsCreateView.as_view(), name='create_fav_thing'),
    url(r'^GetFavThings/(?P<category>[0-9a-f-]+)/(?P<user>[0-9a-f-]+)/$',
        views.GetFavThings.as_view(),
        name='get_fav_thing'),
    url(r'^UpdateThing/(?P<id>[0-9a-f-]+)/$', views.FavThingRetrieveUpdateView.as_view(), name='update_thing'),
    url(r'^DestroyThing/(?P<id>[0-9a-f-]+)/$', views.FavThingDestroy.as_view(), name='destroy_thing'),
]
