from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView
from sourcessay.models import Item
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Item, template_name="index.html"), name='index'),
    #url(r'^admin/', include(admin.site.urls)),
)

# URL patterns below here will only be live in the development environment.
if settings.DEVELOPMENT:
    urlpatterns += patterns("django.views",
        url(r"^media/(.*)$", "static.serve", {
            "document_root": settings.MEDIA_ROOT,
            'show_indexes': True, 
            }),
    )
