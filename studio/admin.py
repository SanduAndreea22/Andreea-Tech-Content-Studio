from django.contrib import admin

from .models import ContactRequest, SampleProject


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("created_at", "name", "business_name", "service", "status")
    list_editable = ("status",)
    list_filter = ("status", "service")
    search_fields = ("name", "email", "business_name")
    date_hierarchy = "created_at"
    list_per_page = 25
    actions = ["mark_sample_sent", "mark_replied"]
    readonly_fields = (
        "created_at", "name", "email", "business_name", "service",
        "what_you_sell", "link", "goal", "message",
    )
    fields = (
        "status", "created_at", "name", "email", "business_name", "service",
        "what_you_sell", "link", "goal", "message",
    )

    def has_add_permission(self, request):
        return False

    @admin.action(description="Mark selected as: ad sent")
    def mark_sample_sent(self, request, queryset):
        queryset.update(status="sample_sent")

    @admin.action(description="Mark selected as: replied")
    def mark_replied(self, request, queryset):
        queryset.update(status="replied")


@admin.register(SampleProject)
class SampleProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "cover", "is_published", "sort_order", "created_at")
    list_editable = ("is_published", "sort_order")
    list_filter = ("category", "is_published")
    search_fields = ("title", "description")
