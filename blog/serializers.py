from rest_framework import serializers
from .models import Category, Tag, Blog, BlogLeads


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'created_at', 'updated_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at']


class BlogListSerializer(serializers.ModelSerializer):
    """Serializer for blog list view"""
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'short_title', 'slug', 'author_username', 'author_full_name',
            'category', 'tags', 'short_description', 'banner_image', 'mobile_image',
            'estimated_time', 'status', 'is_featured', 'is_pinned',
            'views_count', 'likes_count', 'shares_count', 'published_at',
            'created_at', 'updated_at'
        ]
    
    def get_author_full_name(self, obj):
        if obj.author:
            return f"{obj.author.first_name} {obj.author.last_name}".strip() or obj.author.username
        return None


class BlogDetailSerializer(serializers.ModelSerializer):
    """Serializer for blog detail view"""
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_full_name = serializers.SerializerMethodField()
    engagement_score = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'short_title', 'slug', 'author', 'author_username', 'author_full_name',
            'category', 'tags', 'short_description', 'content', 'banner_image', 'mobile_image',
            'estimated_time', 'meta_title', 'meta_description', 'meta_keywords',
            'status', 'is_featured', 'is_pinned',
            'views_count', 'likes_count', 'shares_count', 'engagement_score',
            'published_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'views_count', 'likes_count', 'shares_count', 'published_at']
    
    def get_author_full_name(self, obj):
        if obj.author:
            return f"{obj.author.first_name} {obj.author.last_name}".strip() or obj.author.username
        return None
    
    def get_engagement_score(self, obj):
        return obj.views_count + (obj.likes_count * 2) + (obj.shares_count * 3)


class BlogCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating blogs"""
    class Meta:
        model = Blog
        fields = [
            'title', 'short_title', 'author', 'category', 'tags',
            'short_description', 'content', 'banner_image', 'mobile_image',
            'estimated_time', 'meta_title', 'meta_description', 'meta_keywords',
            'status', 'is_featured', 'is_pinned'
        ]


class BlogLeadsSerializer(serializers.ModelSerializer):
    """Serializer for blog leads"""
    blog_title = serializers.CharField(source='blog.title', read_only=True)
    blog_slug = serializers.CharField(source='blog.slug', read_only=True)
    
    class Meta:
        model = BlogLeads
        fields = [
            'id', 'blog', 'blog_title', 'blog_slug', 'name', 'email', 'phone',
            'company', 'lead_source', 'message', 'is_contacted', 'is_converted',
            'notes', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_refcode',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['is_contacted', 'is_converted', 'notes']


class BlogLeadsCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating blog leads"""
    class Meta:
        model = BlogLeads
        fields = [
            'blog', 'name', 'email', 'phone', 'company', 'lead_source', 'message',
            'utm_source', 'utm_medium', 'utm_campaign', 'utm_refcode'
        ]

