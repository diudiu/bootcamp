from django.conf.urls import url

from messenger import views

urlpatterns = [
    url(r'^$', views.inbox, name='inbox'),
]