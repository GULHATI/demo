from . import views
from django.conf.urls  import *
from django.contrib.auth import views as v
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^loginpage/$', views.gologin, name='gologin'),
    url(r'^login/$', views.signin, name='login'),
    url(r'^sigin/', views.custsignuppage, name='signin'),
    url(r'^partnersigin/', views.partnersignuppage, name='partnersignin'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^logout/$', v.logout, name='logout'),
    url(r'^home/', views.gohome, name='gohome'),
    url(r'^partnerlogin', views.partnerlogin, name='partnerlogin'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^customerdashboard/$',views.customerdashboard,name='customerdashboard'),
    url(r'^supplierdashboard/$',views.supplierdashboard,name = 'supplierdashboard'),
    url(r'^addtechnologies/$',views.add_technologies,name='addtechnologies'),
]