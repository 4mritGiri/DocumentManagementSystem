from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

admin.site.site_header = 'DMS Admin'
admin.site.site_title = 'DMS Admin Portal'
admin.site.index_title = 'Welcome to DMS Admin Portal'

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("dmsApp.urls")),
    path("package/", include("Package.urls")),
    path("document/", include("DocumentApps.urls")),
    path("scheduled-monitoring/", include("ScheduledMonitoring.urls")),
    # path("package-collection/", include("PackageCollection.urls")),
    # path("destruction-eligible/", include("DestructionEligible.urls")),
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

# Add static and media file serving during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

