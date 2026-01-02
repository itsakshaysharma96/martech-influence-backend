from rest_framework import serializers
from .models import CaseStudyCategory, CaseStudy, CaseStudyLead, CaseStudyTag, CaseStudyDynamicField


class CaseStudyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudyCategory
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'created_at', 'updated_at']



class CaseStudyTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudyTag
        fields = ['id', 'name', 'slug', 'created_at']
        
class CaseStudyListSerializer(serializers.ModelSerializer):
    """Serializer for case study list view"""
    category = CaseStudyCategorySerializer(read_only=True)
    tags = CaseStudyTagSerializer(many=True, read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_full_name = serializers.SerializerMethodField()
    dynamic_fields = serializers.SerializerMethodField()
    
    class Meta:
        model = CaseStudy
        fields = [
            'id', 'title', 'slug', 'author_username', 'author_full_name',
            'category', 'tags', 'short_description', 'banner_image', 'logo_image','lp_image',
            'client_name', 'client_industry', 'estimated_time', 'status','dynamic_fields',
            'is_featured', 'is_pinned', 'views_count', 'likes_count',
            'shares_count', 'downloads_count', 'published_at',
            'created_at', 'updated_at'
        ]
    
    def get_author_full_name(self, obj):
        if obj.author:
            return f"{obj.author.first_name} {obj.author.last_name}".strip() or obj.author.username
        return None
    
    def get_dynamic_fields(self, obj):
        qs = obj.dynamic_fields.filter(is_active=True).order_by('sequence')
        return CaseStudyDynamicFieldSerializer(qs, many=True).data

class CaseStudyDynamicFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudyDynamicField
        fields = ['id', 'field_name', 'placeholder', 'sequence', 'is_active']


class CaseStudyDetailSerializer(serializers.ModelSerializer):
    """Serializer for case study detail view"""
    category = CaseStudyCategorySerializer(read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_full_name = serializers.SerializerMethodField()
    engagement_score = serializers.SerializerMethodField()
    dynamic_fields = serializers.SerializerMethodField()
    
    class Meta:
        model = CaseStudy
        fields = [
            'id', 'title', 'slug', 'author', 'author_username', 'author_full_name',
            'category', 'short_description', 'content', 'banner_image', 'logo_image','lp_image',
            'external_link','downloadable_file',
            'client_name', 'client_industry', 'project_duration', 'project_budget',
            'results_summary', 'estimated_time', 'meta_title', 'meta_description',
            'meta_keywords', 'status', 'is_featured', 'is_pinned',
            'views_count', 'likes_count', 'shares_count', 'downloads_count',
            'engagement_score','dynamic_fields', 'published_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'views_count', 'likes_count', 'shares_count', 'downloads_count', 'published_at']
    
    def get_author_full_name(self, obj):
        if obj.author:
            return f"{obj.author.first_name} {obj.author.last_name}".strip() or obj.author.username
        return None
    
    def get_engagement_score(self, obj):
        return obj.views_count + (obj.likes_count * 2) + (obj.shares_count * 3) + (obj.downloads_count * 5)

    def get_dynamic_fields(self, obj):
        qs = obj.dynamic_fields.filter(is_active=True).order_by('sequence')
        return CaseStudyDynamicFieldSerializer(qs, many=True).data


class CaseStudyLeadSerializer(serializers.ModelSerializer):
    """Serializer for case study leads"""
    case_study_title = serializers.CharField(source='case_study.title', read_only=True)
    case_study_slug = serializers.CharField(source='case_study.slug', read_only=True)
    
    class Meta:
        model = CaseStudyLead
        fields = [
            'id', 'case_study', 'case_study_title', 'case_study_slug', 'name', 'email',
            'phone', 'company', 'job_title', 'lead_source', 'message',
            'is_contacted', 'is_converted', 'notes', 'utm_source', 'utm_medium',
            'utm_campaign', 'utm_refcode', 'created_at', 'updated_at'
        ]
        read_only_fields = ['is_contacted', 'is_converted', 'notes']


class CaseStudyLeadCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating case study leads"""
    class Meta:
        model = CaseStudyLead
        fields = ['case_study', 'data']
        extra_kwargs = {
            'case_study': {'required': True},
            'data': {'required': True},
        }

    def validate_data(self, value):
        """Optional: Validate dynamic fields format"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Data must be a JSON object")
        return value


