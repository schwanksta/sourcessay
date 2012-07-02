from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView
from sourcessay.models import Item

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Item, template_name="index.html"), name='index'),
    url(r'^admin/', include(admin.site.urls)),
)
