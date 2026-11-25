from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from studio.sitemaps import PagesSitemap, SamplesSitemap

SITEMAPS = {"pages": PagesSitemap, "samples": SamplesSitemap}

admin.site.site_header = "Andreea Sandu: admin"
admin.site.site_title = "Admin"
admin.site.index_title = "Messages and portfolio"

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="sitemap"),
    path("", include("studio.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
