from django.conf.urls import url

from feeds import views

urlpatterns = [
    url(r'^$', views.feeds, name='feeds'),

    url(r'^load/$', views.load, name='load'),
]