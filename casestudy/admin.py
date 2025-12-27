from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms
from tinymce.widgets import TinyMCE
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import CaseStudyCategory, CaseStudy, CaseStudyLead, CaseStudyTag, CaseStudyDynamicField


class CaseStudyAdminForm(forms.ModelForm):
    """Custom form for Case Study admin with better content field"""
    class Meta:
        model = CaseStudy
        fields = '__all__'
        widgets = {
            'content': TinyMCE(attrs={'cols': 120, 'rows': 80}),
            'short_description': forms.Textarea(attrs={
                'rows': 5,
                'cols': 100,
                'style': 'width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd;',
            }),
            'short_title': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd; font-size: 14px;',
                'placeholder': 'Enter short title...'
            }),
            'results_summary': forms.Textarea(attrs={
                'rows': 4,
                'cols': 100,
                'style': 'width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd;',
            }),
        }


@admin.register(CaseStudyCategory)
class CaseStudyCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active_badge', 'case_study_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'slug', 'description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def is_active_badge(self, obj):
        if obj.is_active:
            return mark_safe('<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">✓ Active</span>')
        return mark_safe('<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">✗ Inactive</span>')
    is_active_badge.short_description = 'Status'

    def case_study_count(self, obj):
        count = obj.case_studies.count()
        return format_html('<strong style="color: #007bff;">{}</strong>', count)
    case_study_count.short_description = 'Case Studies'



@admin.register(CaseStudyTag)
class CaseStudyTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25

    fieldsets = (
        ('Tag Information', {
            'fields': ('name', 'slug')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
class CaseStudyResource(resources.ModelResource):
    class Meta:
        model = CaseStudy
        fields = (
            'id', 'title', 'slug', 'author__username', 'category__name', 'status', 
            'client_name', 'client_industry', 'project_duration', 'project_budget', 'results_summary', 
            'short_description', 'content', 'meta_title', 'meta_description', 'meta_keywords', 
            'created_at', 'published_at'
        )
        export_order = fields


class CaseStudyDynamicFieldInline(admin.TabularInline):
    model = CaseStudyDynamicField
    extra = 1
    fields = ('field_name', 'placeholder','sequence', 'is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    verbose_name = "Dynamic Field"
    verbose_name_plural = "Dynamic Fields"
            
@admin.register(CaseStudy)
class CaseStudyAdmin(ImportExportModelAdmin):
    inlines = [CaseStudyDynamicFieldInline]
    resource_class = CaseStudyResource
    form = CaseStudyAdminForm
    view_on_site = False

    list_display = [
        'title', 'author', 'category', 'status_badge', 
        'created_at', 'published_at'
    ]
    list_filter = ['status', 'category', 'tags', 'client_industry', 'created_at', 'published_at']
    search_fields = ['title', 'short_title', 'content', 'short_description', 'client_name', 'client_industry', 'meta_keywords']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'created_at', 'updated_at', 'banner_image_preview', 'mobile_image_preview', 'logo_image_preview', 'lp_image_preview', 'content_preview'
    ]
    date_hierarchy = 'created_at'
    list_per_page = 25
    filter_horizontal = ['tags']

    # Fieldsets
    fieldsets = (
        ('📝 Basic Information', {
            'fields': ('title', 'slug', 'author', 'category','tags', 'status'),
            'classes': ('wide',),
        }),
        ('👔 Client Information', {
            'fields': ('client_name', 'client_industry', 'project_duration', 'project_budget', 'results_summary'),
            'classes': ('wide',),
        }),
        ('📄 Content', {
            'fields': ('short_description', 'content', 'content_preview'),
            'classes': ('wide',),
        }),
        ('🖼️ Images', {
            'fields': ('banner_image', 'logo_image', 'lp_image'),
            'classes': ('wide',),
        }),
        ('🔍 SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('⚙️ Settings', {
            'fields': ('published_at',)
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # ----------------------------
    # Custom Display Methods
    # ----------------------------
    def title_preview(self, obj):
        title = obj.title or "Untitled"
        if len(title) > 50:
            title = title[:50] + "..."
        return format_html('<strong style="color: #333;">{}</strong>', title)
    title_preview.short_description = 'Title'

    def status_badge(self, obj):
        status_colors = {
            'draft': '#6c757d',
            'published': '#28a745',
            'archived': '#dc3545'
        }
        color = status_colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    # ----------------------------
    # Image Previews
    # ----------------------------
    def banner_image_preview(self, obj):
        if obj.banner_image:
            url = obj.banner_image.url
            name = obj.banner_image.name.split('/')[-1]
            size = getattr(obj.banner_image, 'size', 'Unknown')
            size_str = f"{size / 1024:.1f} KB" if isinstance(size, int) else 'Unknown'
            return format_html(
                '<div style="margin:10px 0; padding:10px; border-radius:8px; background:#f0f4f8;">'
                '<h4>🖼️ Banner Image (Recommended: 300x400)</h4>'
                '<img src="{}" width="150" height="200" style="object-fit:cover; border-radius:4px;" />'
                '<p>📎 {} | Size: {}</p>'
                '<a href="{}" target="_blank">View Full Image</a>'
                '</div>', url, name, size_str, url
            )
        return mark_safe('<p style="color:#999;">🖼️ No banner image uploaded. Recommended: 300x400</p>')
    banner_image_preview.short_description = "Banner Image Preview"

    def logo_image_preview(self, obj):
        if obj.logo_image:
            url = obj.logo_image.url
            return format_html(
                '<div style="margin:10px 0;">'
                '<h4>🏷 Logo Image (Recommended: 250x250)</h4>'
                '<img src="{}" width="125" height="125" style="object-fit:cover; border-radius:4px;" />'
                '</div>', url
            )
        return mark_safe('<p style="color:#999;">🏷 No logo image uploaded. Recommended: 250x250</p>')
    logo_image_preview.short_description = "Logo Image Preview"

    def lp_image_preview(self, obj):
        if obj.lp_image:
            url = obj.lp_image.url
            return format_html(
                '<div style="margin:10px 0;">'
                '<h4>📌 LP Image (Recommended: 600x600)</h4>'
                '<img src="{}" width="150" height="150" style="object-fit:cover; border-radius:4px;" />'
                '</div>', url
            )
        return mark_safe('<p style="color:#999;">📌 No LP image uploaded. Recommended: 600x600</p>')
    lp_image_preview.short_description = "LP Image Preview"

    def mobile_image_preview(self, obj):
        if obj.mobile_image:
            url = obj.mobile_image.url
            return format_html(
                '<div style="margin:10px 0;">'
                '<h4>📱 Mobile Image (Recommended: 768x400)</h4>'
                '<img src="{}" width="150" height="80" style="object-fit:cover; border-radius:4px;" />'
                '</div>', url
            )
        return mark_safe('<p style="color:#999;">📱 No mobile image uploaded. Recommended: 768x400</p>')
    mobile_image_preview.short_description = "Mobile Image Preview"

    # ----------------------------
    # Content Preview
    # ----------------------------
    def content_preview(self, obj):
        if obj.content:
            import re
            content = re.sub(r'<[^>]+>', '', obj.content[:500]) + ("..." if len(obj.content) > 500 else "")
            return format_html(
                '<div style="padding:10px; background:#e0f2fe; border-radius:8px;">{}</div>', content
            )
        return mark_safe('<p style="color:#999;">⚠️ No content available</p>')
    content_preview.short_description = "Content Preview"

    # ----------------------------
    # Admin Actions
    # ----------------------------
    actions = ['make_published', 'make_draft', 'make_archived']

    def make_published(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, f'{updated} case study(ies) marked as published.')
    make_published.short_description = "Mark selected case studies as published"

    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} case study(ies) marked as draft.')
    make_draft.short_description = "Mark selected case studies as draft"

    def make_archived(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} case study(ies) marked as archived.')
    make_archived.short_description = "Mark selected case studies as archived"

@admin.register(CaseStudyLead)
class CaseStudyLeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'case_study', 'dynamic_columns', 'created_at')
    list_filter = ('case_study', 'created_at')
    search_fields = ('data',)
    readonly_fields = (
        'formatted_data',
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Case Study Info', {
            'fields': ('case_study',)
        }),
        ('Lead Data', {
            'fields': ('formatted_data',)
        }),
    )

    def dynamic_columns(self, obj):
        """
        Show JSON fields one by one in list view
        """
        if not obj.data:
            return "-"

        html = ""
        for key, value in obj.data.items():
            html += f"<strong>{key}:</strong> {value}<br>"
        return mark_safe(html)

    dynamic_columns.short_description = "Lead Details"

    def formatted_data(self, obj):
        """
        Show JSON nicely on detail page
        """
        if not obj.data:
            return "-"

        html = "<table style='width:100%; border-collapse: collapse;'>"
        for key, value in obj.data.items():
            html += f"""
                <tr>
                    <td style="padding:8px; border:1px solid #ddd; width:30%; font-weight:bold;">
                        {key}
                    </td>
                    <td style="padding:8px; border:1px solid #ddd;">
                        {value}
                    </td>
                </tr>
            """
        html += "</table>"
        return mark_safe(html)

    formatted_data.short_description = "Submitted Lead Data"