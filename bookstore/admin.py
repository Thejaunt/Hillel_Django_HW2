from django.contrib import admin

from .models import Author, Book, Publisher, Store


class BookInline(admin.TabularInline):
    model = Book


class BookAuthorInline(admin.TabularInline):
    model = Book.authors.through


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["name", "age"]
    list_display = ["name", "age", "id"]
    list_display_links = ["name", "age"]
    fields = [
        "name",
        "age",
    ]
    date_hierarchy = "book__pubdate"
    inlines = [
        BookAuthorInline,
    ]


class BookAdmin(admin.ModelAdmin):
    fields = ["name", "rating", "price", "pages", "pubdate"]
    search_fields = ["rating", "price", "pubdate"]
    filter_vertical = ["authors"]
    list_display = ["rating", "name", "price", "pubdate", "pages", "publisher", "get_authors"]
    list_display_links = ["name"]
    list_select_related = ["publisher"]
    autocomplete_fields = ["authors"]
    ordering = ["-rating", "-pubdate", "price"]
    date_hierarchy = "pubdate"
    list_filter = [
        ("authors", admin.RelatedOnlyFieldListFilter),
        "rating",
        "price",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("authors")

    @staticmethod
    def get_authors(obj):
        return " | ".join([i.name for i in obj.authors.all()])


class PublisherAdmin(admin.ModelAdmin):
    list_display = ["name"]
    ordering = ["name"]
    inlines = [
        BookInline,
    ]


class StoreAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    search_fields = ["name"]
    ordering = ["name"]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Store, StoreAdmin)
