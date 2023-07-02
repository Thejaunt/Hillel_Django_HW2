from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("triangle/", include("triangle.urls")),
    path("__debug__/", include("debug_toolbar.urls"), name="render_panel"),
]
