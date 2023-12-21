from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from log_ingestor.views import LogIngestor
from query_interface.views import QueryInterface, QueryInterfaceUI
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("schema", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "docs",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("logs", LogIngestor.as_view(), name="logs"),
    path("", QueryInterfaceUI.as_view(), name="home"),
    path("query", QueryInterface.as_view(), name="query"),
] + staticfiles_urlpatterns()
