from django.contrib import admin

from .forms import LogTriangleForm
from .models import LogTriangle


class SortByMethodFilter(admin.SimpleListFilter):
    title = "method"
    parameter_name = "method"

    def lookups(self, request, model_admin):
        return [
            ("GET", "GET"),
            ("POST", "POST"),
            ("OTHERS", "OTHERS"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "GET":
            return queryset.filter(method__iexact="GET")
        if self.value() == "POST":
            return queryset.filter(method__iexact="POST")
        if self.value() == "OTHERS":
            return queryset.exclude(method__in=["GET", "POST"])


class LogTriangleAdmin(admin.ModelAdmin):
    form = LogTriangleForm
    fields = ["response_status", "path", "query", "body", "request"]
    readonly_fields = ["timestamp", "method"]
    list_display = ["display_method", "response_status", "timestamp", "path", "query", "body"]
    list_filter = (
        SortByMethodFilter,
        "response_status",
    )
    search_fields = ("path", "response_status")

    def display_method(self, obj):
        return obj.method

    display_method.short_description = "method"


admin.site.register(LogTriangle, LogTriangleAdmin)
