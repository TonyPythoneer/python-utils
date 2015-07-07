from django.conf.urls import url

from app_user import views


urlpatterns = [
    url(r'^signup$', views.signup, name='signup'),
]
