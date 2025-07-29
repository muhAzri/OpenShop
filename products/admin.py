from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "sku",
        "shop",
        "location",
        "category",
        "price",
        "discount",
        "stock",
        "is_available",
        "is_delete",
    ]
    list_filter = ["is_available", "is_delete", "category", "shop", "location"]
    search_fields = ["name", "sku", "description", "shop", "location"]
    list_editable = ["is_available", "stock", "price", "discount"]
    readonly_fields = ["id", "created_at", "updated_at"]
    ordering = ["-created_at"]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("id", "name", "sku", "description", "picture")},
        ),
        ("Shop Details", {"fields": ("shop", "location", "category")}),
        (
            "Pricing & Inventory",
            {"fields": ("price", "discount", "stock", "is_available")},
        ),
        (
            "System Fields",
            {
                "fields": ("is_delete", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ["soft_delete_selected"]

    def soft_delete_selected(self, request, queryset):
        count = queryset.update(is_delete=True)
        self.message_user(
            request, f"{count} product(s) were successfully soft deleted."
        )

    soft_delete_selected.short_description = "Soft delete selected products"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.is_delete:
            form.base_fields["is_delete"].help_text = (
                "This product is soft deleted. Uncheck to restore."
            )
        return form
