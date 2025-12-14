from django.contrib import admin
from django.utils.html import format_html
from .models import SocialMedia


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = [
        'platform_display', 'url_link', 'icon_preview', 'is_active', 'is_active_badge', 'created_at'
    ]
    list_filter = ['platform', 'is_active', 'created_at']
    search_fields = ['platform', 'url', 'description']
    readonly_fields = ['created_at', 'updated_at', 'icon_preview']
    list_editable = ['is_active']
    list_per_page = 25
    
    fieldsets = (
        ('📱 Social Media Information', {
            'fields': ('platform', 'url', 'icon', 'icon_preview', 'is_active'),
            'classes': ('wide',),
        }),
        ('📝 Additional Information', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def platform_display(self, obj):
        platform_name = obj.display_name
        colors = {
            'facebook': '#1877f2',
            'instagram': '#e4405f',
            'twitter': '#1da1f2',
            'linkedin': '#0077b5',
            'youtube': '#ff0000',
            'pinterest': '#bd081c',
            'tiktok': '#000000',
            'snapchat': '#fffc00',
            'whatsapp': '#25d366',
            'telegram': '#0088cc',
            'discord': '#5865f2',
            'github': '#181717',
            'behance': '#1769ff',
            'dribbble': '#ea4c89',
            'medium': '#000000',
            'reddit': '#ff4500',
            'other': '#6c757d'
        }
        color = colors.get(obj.platform, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, platform_name
        )
    platform_display.short_description = 'Platform'

    def url_link(self, obj):
        if obj.url:
            return format_html(
                '<a href="{}" target="_blank" style="color: #007bff; text-decoration: none; font-weight: bold;">🔗 {}</a>',
                obj.url, obj.url[:50] + "..." if len(obj.url) > 50 else obj.url
            )
        return format_html('<span style="color: #999;">—</span>')
    url_link.short_description = 'URL'

    def icon_preview(self, obj):
        if obj.icon:
            file_name = obj.icon.name.split('/')[-1]
            # Check if it's an image file
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico']
            is_image = any(file_name.lower().endswith(ext) for ext in image_extensions)
            
            if is_image:
                return format_html(
                    '<div style="margin: 10px 0;">'
                    '<img src="{}" width="50" height="50" style="object-fit: contain; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />'
                    '<p style="margin-top: 5px; color: #666; font-size: 11px;">{}</p>'
                    '</div>',
                    obj.icon.url, file_name
                )
            else:
                return format_html(
                    '<div style="padding: 10px; background: #f8f9fa; border-radius: 5px; margin: 5px 0;">'
                    '<p style="margin: 0; color: #333; font-weight: bold;">📎 {}</p>'
                    '<a href="{}" target="_blank" style="color: #007bff; text-decoration: none; font-size: 12px;">View File</a>'
                    '</div>',
                    file_name, obj.icon.url
                )
        return format_html('<span style="color: #999;">No icon uploaded</span>')
    icon_preview.short_description = 'Icon Preview'

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">✓ Active</span>')
        return format_html('<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">✗ Inactive</span>')
    is_active_badge.short_description = 'Status'

    actions = ['activate', 'deactivate']

    def activate(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} social media link(s) activated.')
    activate.short_description = "Activate selected links"

    def deactivate(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} social media link(s) deactivated.')
    deactivate.short_description = "Deactivate selected links"
