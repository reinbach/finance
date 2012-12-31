from coffin.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^robots.txt$', direct_to_template, {'template':'robots.txt', 'mimetype':'text/plain'}),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', 'core.views.home', name='home'),
)

urlpatterns += staticfiles_urlpatterns()