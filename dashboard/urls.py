from . import views
from django.conf.urls  import *
from django.contrib.auth import views as v
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^loginpage/$', views.gologin, name='gologin'),
    url(r'^login/$', views.signin, name='login'),
    url(r'^sigin/', views.loginpage, name='signin'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^logout/$', v.logout, name='logout'),
    url(r'^home/', views.gohome, name='gohome'),

]