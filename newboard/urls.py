from django.conf.urls import url, include
from . import views

app_name = 'myboard'

urlpatterns = [
    url(r'^$', views.boardMain, name="newboard" ),
    url(r'^boardWrite', views.boardWrite),
    url(r'^boardDetail', views.boardDetail, name="boardDetail"),
    url(r'^boardUpdate', views.boardUpdate),
    url(r'^insertData', views.insertData),
    url(r'^updateData', views.updateData),
    url(r'^deleteData', views.deleteData),
    url(r'^test', views.test ),
]
