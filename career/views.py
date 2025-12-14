from rest_framework import viewsets, status
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from martech_influence_backend.utils import create_response
from .models import JobPosting, JobApplication
from .serializers import (
    JobPostingListSerializer, JobPostingDetailSerializer,
    JobApplicationCreateSerializer
)


class JobPostingViewSet(viewsets.ViewSet):
    """
    ViewSet for Job Posting - GET operations only
    """
    
    def get_queryset(self):
        queryset = JobPosting.objects.select_related(
            'department', 'category', 'job_type', 'location', 'recruiter'
        ).filter(status='published')
        
        # Skip filtering during schema generation
        if getattr(self, 'swagger_fake_view', False) or not hasattr(self, 'request') or self.request is None:
            return queryset
        
        # Filter by department
        department = self.request.query_params.get('department', None)
        if department:
            queryset = queryset.filter(department__slug=department)
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by job type
        job_type = self.request.query_params.get('job_type', None)
        if job_type:
            queryset = queryset.filter(job_type__slug=job_type)
        
        # Filter by location
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__slug=location)
        
        # Filter by remote
        is_remote = self.request.query_params.get('is_remote', None)
        if is_remote is not None:
            queryset = queryset.filter(location__is_remote=is_remote.lower() == 'true')
        
        # Filter by experience level
        experience_level = self.request.query_params.get('experience_level', None)
        if experience_level:
            queryset = queryset.filter(experience_level=experience_level)
        
        # Filter by featured
        is_featured = self.request.query_params.get('is_featured', None)
        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured.lower() == 'true')
        
        # Filter by urgent
        is_urgent = self.request.query_params.get('is_urgent', None)
        if is_urgent is not None:
            queryset = queryset.filter(is_urgent=is_urgent.lower() == 'true')
        
        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(short_title__icontains=search) |
                Q(short_description__icontains=search) |
                Q(job_description__icontains=search) |
                Q(skills_required__icontains=search)
            )
        
        # Order by
        ordering = self.request.query_params.get('ordering', '-created_at')
        queryset = queryset.order_by(ordering)
        
        return queryset
    
    def list(self, request):
        """List all published job postings with pagination"""
        from rest_framework.pagination import PageNumberPagination
        
        queryset = self.get_queryset()
        
        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(queryset, request)
        
        if page is not None:
            serializer = JobPostingListSerializer(page, many=True)
            paginated_response = paginator.get_paginated_response(serializer.data)
            
            return create_response(
                status_code=status.HTTP_200_OK,
                message="Job postings retrieved successfully",
                message_code="JOB_POSTINGS_RETRIEVED",
                data=paginated_response.data.get('results', []),
                count=paginated_response.data.get('count', 0),
                next_link=paginated_response.data.get('next'),
                previous_link=paginated_response.data.get('previous')
            )
        
        serializer = JobPostingListSerializer(queryset, many=True)
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Job postings retrieved successfully",
            message_code="JOB_POSTINGS_RETRIEVED",
            data=serializer.data
        )
    
    def retrieve(self, request, pk=None):
        """Retrieve a single job posting"""
        try:
            job_posting = JobPosting.objects.select_related(
                'department', 'category', 'job_type', 'location', 'recruiter'
            ).get(pk=pk, status='published')
        except JobPosting.DoesNotExist:
            return create_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Job posting not found",
                message_code="JOB_POSTING_NOT_FOUND",
                status=False
            )
        
        # Increment views count
        job_posting.views_count += 1
        job_posting.save(update_fields=['views_count'])
        
        serializer = JobPostingDetailSerializer(job_posting)
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Job posting retrieved successfully",
            message_code="JOB_POSTING_RETRIEVED",
            data=serializer.data
        )


class JobApplicationViewSet(viewsets.ViewSet):
    """
    ViewSet for Job Application - CREATE operation only
    """
    
    @swagger_auto_schema(
        operation_description="""
        Submit a new job application.
        
        **Content Type:** `multipart/form-data` (Required for file uploads)
        
        **Note:** This endpoint accepts file uploads (resume, cover_letter), so you must use `multipart/form-data` instead of `application/json`.
        
        **Headers:**
        - `Content-Type: multipart/form-data` (Required)
        
        **Field Requirements:**
        - All fields are **optional** (can be null/blank)
        - However, it's recommended to provide at least `job_posting`, `first_name`, `last_name`, `email`, and `resume`
        
        **Application Source Options:**
        - `website` - Website (default)
        - `linkedin` - LinkedIn
        - `indeed` - Indeed
        - `referral` - Referral
        - `other` - Other
        
        **File Upload Fields:**
        - `resume` - Resume file (PDF, DOC, DOCX recommended)
        - `cover_letter` - Cover letter file (PDF, DOC, DOCX recommended)
        
        **Alternative to File Upload:**
        - `cover_letter_text` - Text content of cover letter (if not uploading file)
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'job_posting': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='Job Posting ID (optional) - ID of the job you are applying for',
                    example=1
                ),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name (optional, max 100 characters)', example='John'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name (optional, max 100 characters)', example='Doe'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Email address (optional)', example='john.doe@example.com'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number (optional, max 20 characters)', example='+1234567890'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='Street address (optional)', example='123 Main St'),
                'city': openapi.Schema(type=openapi.TYPE_STRING, description='City (optional, max 100 characters)', example='New York'),
                'state': openapi.Schema(type=openapi.TYPE_STRING, description='State (optional, max 100 characters)', example='NY'),
                'country': openapi.Schema(type=openapi.TYPE_STRING, description='Country (optional, max 100 characters)', example='USA'),
                'zip_code': openapi.Schema(type=openapi.TYPE_STRING, description='ZIP/Postal code (optional, max 20 characters)', example='10001'),
                'current_company': openapi.Schema(type=openapi.TYPE_STRING, description='Current company (optional, max 200 characters)', example='Current Corp'),
                'current_position': openapi.Schema(type=openapi.TYPE_STRING, description='Current position (optional, max 200 characters)', example='Software Engineer'),
                'years_of_experience': openapi.Schema(type=openapi.TYPE_INTEGER, description='Years of experience (optional)', example=5),
                'current_salary': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Current salary (optional)', example=75000.00),
                'expected_salary': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description='Expected salary (optional)', example=90000.00),
                'notice_period': openapi.Schema(type=openapi.TYPE_STRING, description='Notice period (optional, max 100 characters)', example='2 weeks'),
                'resume': openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description='Resume file (optional) - PDF, DOC, or DOCX file',
                    format=openapi.FORMAT_BINARY
                ),
                'cover_letter': openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description='Cover letter file (optional) - PDF, DOC, or DOCX file',
                    format=openapi.FORMAT_BINARY
                ),
                'portfolio_url': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description='Portfolio URL (optional)', example='https://portfolio.example.com'),
                'linkedin_url': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description='LinkedIn profile URL (optional)', example='https://linkedin.com/in/johndoe'),
                'github_url': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description='GitHub profile URL (optional)', example='https://github.com/johndoe'),
                'cover_letter_text': openapi.Schema(type=openapi.TYPE_STRING, description='Cover letter text content (optional, if not uploading file)', example='Dear Hiring Manager...'),
                'why_interested': openapi.Schema(type=openapi.TYPE_STRING, description='Why are you interested in this role? (optional)', example='I am passionate about...'),
                'availability_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Date available to start (optional, YYYY-MM-DD)', example='2024-01-15'),
                'source': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['website', 'linkedin', 'indeed', 'referral', 'other'],
                    description='Application source (optional, default: "website")',
                    example='website'
                ),
                'utm_source': openapi.Schema(type=openapi.TYPE_STRING, description='UTM source (optional)', example='google'),
                'utm_medium': openapi.Schema(type=openapi.TYPE_STRING, description='UTM medium (optional)', example='cpc'),
                'utm_campaign': openapi.Schema(type=openapi.TYPE_STRING, description='UTM campaign (optional)', example='job_posting'),
                'utm_refcode': openapi.Schema(type=openapi.TYPE_STRING, description='UTM reference code (optional)', example='REF789'),
            }
        ),
        consumes=['multipart/form-data'],
        responses={
            201: openapi.Response(description='Job application submitted successfully'),
            400: openapi.Response(description='Bad request - validation errors')
        },
        tags=['Job Applications']
    )
    def create(self, request):
        """Create a new job application"""
        serializer = JobApplicationCreateSerializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save()
            # Increment applications count for the job posting
            if application.job_posting:
                application.job_posting.applications_count += 1
                application.job_posting.save(update_fields=['applications_count'])
            
            return create_response(
                status_code=status.HTTP_201_CREATED,
                message="Job application submitted successfully",
                message_code="JOB_APPLICATION_CREATED",
                data=serializer.data
            )
        return create_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Job application submission failed",
            message_code="JOB_APPLICATION_CREATION_FAILED",
            status=False,
            data=serializer.errors
        )
