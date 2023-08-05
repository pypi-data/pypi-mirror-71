from __future__ import annotations

import threading

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.urls import reverse
from django.utils.html import format_html

from . import models

globals = threading.local()


@admin.register(models.View)
class ViewAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name", "owner", "open_view", "description"]}),
        (
            "Public",
            {
                "fields": [
                    "public",
                    "public_slug",
                    "public_link",
                    "google_sheets_formula",
                ]
            },
        ),
        ("Query", {"fields": ["model_name", "fields", "query"]}),
        ("Internal", {"fields": ["id", "created_time"]}),
    ]
    readonly_fields = [
        "open_view",
        "public_link",
        "google_sheets_formula",
        "id",
        "created_time",
    ]
    list_display = ["__str__", "owner", "public"]

    def get_readonly_fields(self, request, obj):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if request.user.has_perm("data_browser.make_view_public"):
            return readonly_fields
        elif obj and obj.public:
            return flatten_fieldsets(self.get_fieldsets(request, obj))
        else:
            return readonly_fields + ["public", "public_slug"]

    def get_fieldsets(self, request, obj=None):
        res = super().get_fieldsets(request, obj)
        if not request.user.has_perm("data_browser.make_view_public"):
            res = [fs for fs in res if fs[0] != "Public"]
        return res

    def change_view(self, request, *args, **kwargs):
        globals.request = request
        return super().change_view(request, *args, **kwargs)

    @staticmethod
    def open_view(obj):
        if not obj.model_name:
            return "N/A"
        url = obj.get_query().get_url("html")
        return format_html(f'<a href="{url}">view</a>')

    @staticmethod
    def public_link(obj):
        if obj.public:
            if getattr(settings, "DATA_BROWSER_ALLOW_PUBLIC", False):
                url = reverse(
                    "data_browser:view", kwargs={"pk": obj.public_slug, "media": "csv"}
                )
                return globals.request.build_absolute_uri(url)
            else:
                return "Public URL's are disabled in Django settings."
        else:
            return "N/A"

    @staticmethod
    def google_sheets_formula(obj):
        if obj.public:
            if getattr(settings, "DATA_BROWSER_ALLOW_PUBLIC", False):
                url = reverse(
                    "data_browser:view", kwargs={"pk": obj.public_slug, "media": "csv"}
                )
                url = globals.request.build_absolute_uri(url)
                return f'=importdata("{url}")'
            else:
                return "Public URL's are disabled in Django settings."
        else:
            return "N/A"

    def get_changeform_initial_data(self, request):
        get_results = super().get_changeform_initial_data(request)
        get_results["owner"] = request.user.pk
        return get_results
