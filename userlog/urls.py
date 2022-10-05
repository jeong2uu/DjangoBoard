from django.conf.urls import url, include
from . import views

app_name = "userlog"

urlpatterns = [
    url(r'^$', views.login_view, name="login" ),
    url(r'^logout/', views.logout_view, name="logout"),
    url(r'^signup/', views.signup_view, name="signup"),
    url(r'^duplicate_id', views.duplicate_id, name="duplicate_id"),
]
