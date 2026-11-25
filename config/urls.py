from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Andreea Sandu: admin"
admin.site.site_title = "Admin"
admin.site.index_title = "Messages and portfolio"

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include("studio.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
