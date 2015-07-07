from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', 'app_user.views.home', name='home'),
    url(r'^u/', include('app_user.urls', namespace='user')),
]
