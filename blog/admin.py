from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms
from tinymce.widgets import TinyMCE
from .models import Category, Tag, Blog, BlogLeads


class BlogAdminForm(forms.ModelForm):
    """Custom form for Blog admin with better content field"""
    class Meta:
        model = Blog
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
        }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active_badge', 'blog_count', 'created_at']
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

    def blog_count(self, obj):
        count = obj.blogs.count()
        return format_html('<strong style="color: #007bff;">{}</strong>', count)
    blog_count.short_description = 'Blogs'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'blog_count', 'created_at']
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

    def blog_count(self, obj):
        count = obj.blogs.count()
        return format_html('<strong style="color: #007bff;">{}</strong>', count)
    blog_count.short_description = 'Blogs'


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = [
        'title_preview', 'short_title_preview', 'author', 'category', 'status_badge',
        'is_featured', 'is_pinned', 'is_featured_badge', 'estimated_time_display', 'views_count',
        'engagement_score', 'created_at', 'published_at'
    ]
    list_filter = ['status', 'is_featured', 'is_pinned', 'category', 'tags', 'created_at', 'published_at']
    search_fields = ['title', 'short_title', 'content', 'short_description', 'meta_keywords']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'created_at', 'updated_at', 'views_count', 'likes_count',
        'shares_count', 'banner_image_preview', 'mobile_image_preview', 'engagement_score_display', 'content_preview'
    ]
    filter_horizontal = ['tags']
    date_hierarchy = 'created_at'
    list_per_page = 25
    list_editable = ['is_featured', 'is_pinned']

    fieldsets = (
        ('📝 Basic Information', {
            'fields': ('title', 'short_title', 'slug', 'author', 'category', 'tags', 'status'),
            'classes': ('wide',),
        }),
        ('📄 Content', {
            'fields': ('short_description', 'content', 'content_preview', 'estimated_time'),
            'classes': ('wide',),
        }),
        ('🖼️ Images', {
            'fields': ('banner_image', 'banner_image_preview', 'mobile_image', 'mobile_image_preview'),
            'classes': ('wide',),
        }),
        ('🔍 SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('⚙️ Settings', {
            'fields': ('is_featured', 'is_pinned', 'published_at')
        }),
        ('📊 Engagement Metrics', {
            'fields': ('views_count', 'likes_count', 'shares_count', 'engagement_score_display'),
            'classes': ('collapse',)
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def title_preview(self, obj):
        title = obj.title or "Untitled"
        if len(title) > 50:
            title = title[:50] + "..."
        return format_html('<strong style="color: #333;">{}</strong>', title)
    title_preview.short_description = 'Title'

    def short_title_preview(self, obj):
        if obj.short_title:
            short_title = obj.short_title[:60] + "..." if len(obj.short_title) > 60 else obj.short_title
            return format_html(
                '<span style="color: #666; font-size: 12px; padding: 4px 8px; background: #f8f9fa; border-radius: 4px; display: inline-block;">{}</span>',
                short_title
            )
        return mark_safe('<span style="color: #999;">—</span>')
    short_title_preview.short_description = 'Short Title'

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

    def is_featured_badge(self, obj):
        if obj.is_featured:
            return mark_safe('<span style="background-color: #ffc107; color: #000; padding: 3px 8px; border-radius: 10px; font-size: 10px;">⭐ Featured</span>')
        return mark_safe('<span style="color: #999;">—</span>')
    is_featured_badge.short_description = 'Featured'

    def estimated_time_display(self, obj):
        if obj.estimated_time:
            return format_html(
                '<span style="background-color: #17a2b8; color: white; padding: 3px 8px; border-radius: 10px; font-size: 11px;">⏱ {} min</span>',
                obj.estimated_time
            )
        return mark_safe('<span style="color: #999;">—</span>')
    estimated_time_display.short_description = 'Read Time'

    def engagement_score(self, obj):
        score = obj.views_count + (obj.likes_count * 2) + (obj.shares_count * 3)
        if score > 100:
            color = '#28a745'
        elif score > 50:
            color = '#ffc107'
        else:
            color = '#6c757d'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; border-radius: 12px; font-weight: bold;">{}</span>',
            color, score
        )
    engagement_score.short_description = 'Engagement'

    def engagement_score_display(self, obj):
        score = obj.views_count + (obj.likes_count * 2) + (obj.shares_count * 3)
        return format_html(
            '<div style="padding: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; text-align: center;">'
            '<h3 style="margin: 0; font-size: 32px;">{}</h3>'
            '<p style="margin: 5px 0 0 0; font-size: 12px;">Total Engagement Score</p>'
            '</div>',
            score
        )
    engagement_score_display.short_description = 'Engagement Score'

    def banner_image_preview(self, obj):
        if obj.banner_image:
            image_url = obj.banner_image.url
            file_name = obj.banner_image.name.split('/')[-1]
            file_size = obj.banner_image.size if hasattr(obj.banner_image, 'size') else 'Unknown'
            # Format file size
            if isinstance(file_size, int):
                if file_size < 1024:
                    size_str = f"{file_size} B"
                elif file_size < 1024 * 1024:
                    size_str = f"{file_size / 1024:.1f} KB"
                else:
                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
            else:
                size_str = 'Unknown'

            return format_html(
                '<div style="margin: 15px 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">'
                '<h4 style="margin: 0 0 15px 0; color: white; font-size: 16px; font-weight: bold;">🖼️ Banner Image (Desktop)</h4>'
                '<img src="{}" width="100%" max-width="600" height="300" style="object-fit: cover; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); border: 3px solid white; margin-bottom: 15px;" />'
                '<div style="padding: 12px; background: rgba(255,255,255,0.95); border-radius: 6px;">'
                '<p style="margin: 5px 0; color: #333; font-weight: bold;">📎 {}</p>'
                '<p style="margin: 5px 0; color: #666; font-size: 12px;">Size: {}</p>'
                '<a href="{}" target="_blank" style="display: inline-block; margin-top: 8px; padding: 8px 18px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; font-size: 13px; font-weight: bold;">🔗 View Full Image</a>'
                '</div>'
                '</div>',
                image_url, file_name, size_str, image_url
            )
        return mark_safe(
            '<div style="padding: 30px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 8px; text-align: center; border: 2px dashed #ccc;">'
            '<p style="color: #999; font-size: 14px; margin: 0;">🖼️ No banner image uploaded</p>'
            '<p style="color: #bbb; font-size: 12px; margin: 5px 0 0 0;">Recommended: Wide format (1920x600px)</p>'
            '</div>'
        )
    banner_image_preview.short_description = "🖼️ Banner Image Preview"

    def mobile_image_preview(self, obj):
        if obj.mobile_image:
            image_url = obj.mobile_image.url
            file_name = obj.mobile_image.name.split('/')[-1]
            file_size = obj.mobile_image.size if hasattr(obj.mobile_image, 'size') else 'Unknown'
            # Format file size
            if isinstance(file_size, int):
                if file_size < 1024:
                    size_str = f"{file_size} B"
                elif file_size < 1024 * 1024:
                    size_str = f"{file_size / 1024:.1f} KB"
                else:
                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
            else:
                size_str = 'Unknown'

            return format_html(
                '<div style="margin: 15px 0; padding: 20px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">'
                '<h4 style="margin: 0 0 15px 0; color: white; font-size: 16px; font-weight: bold;">📱 Mobile Image</h4>'
                '<img src="{}" width="100%" max-width="400" height="250" style="object-fit: cover; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); border: 3px solid white; margin-bottom: 15px;" />'
                '<div style="padding: 12px; background: rgba(255,255,255,0.95); border-radius: 6px;">'
                '<p style="margin: 5px 0; color: #333; font-weight: bold;">📎 {}</p>'
                '<p style="margin: 5px 0; color: #666; font-size: 12px;">Size: {}</p>'
                '<a href="{}" target="_blank" style="display: inline-block; margin-top: 8px; padding: 8px 18px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; font-size: 13px; font-weight: bold;">🔗 View Full Image</a>'
                '</div>'
                '</div>',
                image_url, file_name, size_str, image_url
            )
        return mark_safe(
            '<div style="padding: 30px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 8px; text-align: center; border: 2px dashed #ccc;">'
            '<p style="color: #999; font-size: 14px; margin: 0;">📱 No mobile image uploaded</p>'
            '<p style="color: #bbb; font-size: 12px; margin: 5px 0 0 0;">Recommended: Mobile format (768x400px)</p>'
            '</div>'
        )
    mobile_image_preview.short_description = "📱 Mobile Image Preview"

    def content_preview(self, obj):
        if obj.content:
            content = obj.content[:500] + "..." if len(obj.content) > 500 else obj.content
            # Strip HTML tags for preview
            import re
            clean_content = re.sub(r'<[^>]+>', '', content)
            return format_html(
                '<div style="max-height: 350px; overflow-y: auto; padding: 20px; background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%); border-radius: 12px; border: 2px solid #0ea5e9; margin: 15px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">'
                '<h4 style="margin: 0 0 15px 0; color: #0369a1; font-size: 16px; font-weight: bold; display: flex; align-items: center;">'
                '<span style="margin-right: 8px;">📄</span> Content Preview</h4>'
                '<div style="white-space: pre-wrap; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 14px; line-height: 1.8; color: #1e293b; background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #0ea5e9;">{}</div>'
                '</div>',
                clean_content
            )
        return mark_safe(
            '<div style="padding: 20px; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 8px; text-align: center; border: 2px dashed #f59e0b;">'
            '<p style="color: #92400e; font-size: 14px; margin: 0; font-weight: 500;">⚠️ No content available</p>'
            '</div>'
        )
    content_preview.short_description = "📄 Content Preview"

    actions = ['make_published', 'make_draft', 'make_archived']

    def make_published(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, f'{updated} blog(s) marked as published.')
    make_published.short_description = "Mark selected blogs as published"

    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} blog(s) marked as draft.')
    make_draft.short_description = "Mark selected blogs as draft"

    def make_archived(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} blog(s) marked as archived.')
    make_archived.short_description = "Mark selected blogs as archived"


@admin.register(BlogLeads)
class BlogLeadsAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog', 'dynamic_columns', 'created_at')
    readonly_fields = ('formatted_data','created_at', 'updated_at')
    list_filter = ('blog', 'created_at')
    search_fields = ('data',)

    fieldsets = (
        ('Blog Info', {
            'fields': ('blog',)
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