from rest_framework import serializers
from .models import (
    Department, JobCategory, JobLocation, JobType,
    JobPosting, JobApplication
)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'created_at', 'updated_at']


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'created_at', 'updated_at']


class JobLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobLocation
        fields = ['id', 'name', 'slug', 'city', 'state', 'country', 'is_remote', 'is_active', 'created_at', 'updated_at']


class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'created_at', 'updated_at']


class JobPostingListSerializer(serializers.ModelSerializer):
    """Serializer for job posting list view"""
    department = DepartmentSerializer(read_only=True)
    category = JobCategorySerializer(read_only=True)
    job_type = JobTypeSerializer(read_only=True)
    location = JobLocationSerializer(read_only=True)
    recruiter_username = serializers.CharField(source='recruiter.username', read_only=True)
    
    class Meta:
        model = JobPosting
        fields = [
            'id', 'title', 'short_title', 'slug', 'department', 'category',
            'job_type', 'location', 'recruiter_username', 'short_description',
            'salary_min', 'salary_max', 'salary_currency', 'salary_period',
            'experience_level', 'experience_years_min', 'experience_years_max',
            'education_required', 'application_deadline', 'is_featured',
            'is_urgent', 'views_count', 'applications_count', 'published_at',
            'created_at', 'updated_at'
        ]


class JobPostingDetailSerializer(serializers.ModelSerializer):
    """Serializer for job posting detail view"""
    department = DepartmentSerializer(read_only=True)
    category = JobCategorySerializer(read_only=True)
    job_type = JobTypeSerializer(read_only=True)
    location = JobLocationSerializer(read_only=True)
    recruiter_username = serializers.CharField(source='recruiter.username', read_only=True)
    recruiter_full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = JobPosting
        fields = [
            'id', 'title', 'short_title', 'slug', 'department', 'category',
            'job_type', 'location', 'recruiter', 'recruiter_username', 'recruiter_full_name',
            'short_description', 'job_description', 'responsibilities', 'requirements',
            'preferred_qualifications', 'skills_required', 'salary_min', 'salary_max',
            'salary_currency', 'salary_period', 'benefits', 'experience_level',
            'experience_years_min', 'experience_years_max', 'education_required',
            'application_deadline', 'application_url', 'application_email',
            'application_instructions', 'is_featured', 'is_pinned', 'is_urgent',
            'meta_title', 'meta_description', 'meta_keywords', 'views_count',
            'applications_count', 'shares_count', 'published_at', 'created_at', 'updated_at'
        ]
    
    def get_recruiter_full_name(self, obj):
        if obj.recruiter:
            return f"{obj.recruiter.first_name} {obj.recruiter.last_name}".strip() or obj.recruiter.username
        return None


class JobApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating job applications"""
    class Meta:
        model = JobApplication
        fields = [
            'job_posting', 'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'state', 'country', 'zip_code',
            'current_company', 'current_position', 'years_of_experience',
            'current_salary', 'expected_salary', 'notice_period',
            'resume', 'cover_letter', 'portfolio_url', 'linkedin_url',
            'github_url', 'cover_letter_text', 'why_interested',
            'availability_date', 'source', 'utm_source', 'utm_medium',
            'utm_campaign', 'utm_refcode'
        ]

