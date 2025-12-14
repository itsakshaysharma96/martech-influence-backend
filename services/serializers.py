from rest_framework import serializers
from .models import ServiceCategory, Service, ServiceLead


class ServiceCategorySerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'slug', 'description', 'icon', 'icon_url', 'is_active', 'created_at', 'updated_at']
    
    def get_icon_url(self, obj):
        if obj.icon:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.icon.url)
            return obj.icon.url
        return None


class ServiceListSerializer(serializers.ModelSerializer):
    """Serializer for service list view"""
    category = ServiceCategorySerializer(read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_full_name = serializers.SerializerMethodField()
    banner_image_url = serializers.SerializerMethodField()
    mobile_image_url = serializers.SerializerMethodField()
    icon_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
            'id', 'title', 'short_title', 'slug', 'category', 'author_username', 'author_full_name',
            'short_description', 'banner_image', 'banner_image_url', 'mobile_image', 'mobile_image_url',
            'icon', 'icon_url', 'price_starting_from', 'price_currency', 'price_period',
            'is_free', 'has_custom_pricing', 'duration', 'delivery_time', 'service_type',
            'status', 'is_featured', 'is_pinned', 'is_popular', 'views_count',
            'inquiries_count', 'likes_count', 'published_at', 'created_at', 'updated_at'
        ]
    
    def get_author_full_name(self, obj):
        if obj.author:
            return f"{obj.author.first_name} {obj.author.last_name}".strip() or obj.author.username
        return None
    
    def get_banner_image_url(self, obj):
        if obj.banner_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.banner_image.url)
            return obj.banner_image.url
        return None
    
    def get_mobile_image_url(self, obj):
        if obj.mobile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.mobile_image.url)
            return obj.mobile_image.url
        return None
    
    def get_icon_url(self, obj):
        if obj.icon:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.icon.url)
            return obj.icon.url
        return None


class ServiceDetailSerializer(serializers.ModelSerializer):
    """Serializer for service detail view"""
    category = ServiceCategorySerializer(read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_full_name = serializers.SerializerMethodField()
    banner_image_url = serializers.SerializerMethodField()
    mobile_image_url = serializers.SerializerMethodField()
    icon_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
            'id', 'title', 'short_title', 'slug', 'category', 'author', 'author_username', 'author_full_name',
            'short_description', 'description', 'features', 'benefits', 'banner_image', 'banner_image_url',
            'mobile_image', 'mobile_image_url', 'icon', 'icon_url', 'price_starting_from', 'price_currency',
            'price_period', 'is_free', 'has_custom_pricing', 'duration', 'delivery_time', 'service_type',
            'meta_title', 'meta_description', 'meta_keywords', 'status', 'is_featured', 'is_pinned',
            'is_popular', 'views_count', 'inquiries_count', 'likes_count', 'published_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'views_count', 'inquiries_count', 'likes_count', 'published_at']
    
    def get_author_full_name(self, obj):
        if obj.author:
            return f"{obj.author.first_name} {obj.author.last_name}".strip() or obj.author.username
        return None
    
    def get_banner_image_url(self, obj):
        if obj.banner_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.banner_image.url)
            return obj.banner_image.url
        return None
    
    def get_mobile_image_url(self, obj):
        if obj.mobile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.mobile_image.url)
            return obj.mobile_image.url
        return None
    
    def get_icon_url(self, obj):
        if obj.icon:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.icon.url)
            return obj.icon.url
        return None


class ServiceLeadCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating service leads"""
    class Meta:
        model = ServiceLead
        fields = [
            'service', 'inquiry_type', 'lead_source', 'full_name', 'email', 'phone',
            'company', 'job_title', 'message', 'budget_range', 'timeline',
            'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'
        ]

