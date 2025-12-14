from rest_framework import serializers
from .models import SocialMedia


class SocialMediaSerializer(serializers.ModelSerializer):
    """Serializer for social media links"""
    display_name = serializers.CharField(source='display_name', read_only=True)
    icon_url = serializers.SerializerMethodField()
    
    class Meta:
        model = SocialMedia
        fields = [
            'id', 'platform', 'display_name', 'url', 'icon', 'icon_url',
            'is_active', 'description', 'created_at', 'updated_at'
        ]
    
    def get_icon_url(self, obj):
        if obj.icon:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.icon.url)
            return obj.icon.url
        return None
