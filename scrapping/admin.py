from django.contrib import admin

from .models import Author, Quote, Tag


class QuoteAdmin(admin.ModelAdmin):
    fields = ["title", "author", ]
    list_display = ["title", "author", "get_tags"]
    list_display_links = ["title"]
    list_select_related = ["author"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("tags")

    @staticmethod
    def get_tags(obj):
        return ", ".join([i.name for i in obj.tags.all()])


admin.site.register(Author)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Tag)
