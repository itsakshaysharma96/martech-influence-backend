from django.contrib import admin
from .models import PrivacyPolicy
from django.db import models
from tinymce.widgets import TinyMCE
# Register your models here.
@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "version",
        "is_active",
        "published_at",
    )
    list_filter = ("is_active",)
    search_fields = ("title", "version")
    ordering = ("-published_at",)

    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE(attrs={"cols": 120, "rows": 80})
        }
    }