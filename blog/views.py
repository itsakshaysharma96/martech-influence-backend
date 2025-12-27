from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from martech_influence_backend.utils import create_response
from .models import Blog, BlogLeads, BlogDynamicField
from .serializers import (
    BlogListSerializer, BlogDetailSerializer,
    BlogLeadsCreateSerializer, BlogDynamicFieldSerializer
)


class BlogViewSet(viewsets.ViewSet):
    """
    ViewSet for Blog - GET operations only
    """
    
    def get_queryset(self):
        queryset = Blog.objects.select_related('author', 'category').prefetch_related('tags').filter(status='published')
        
        # Skip filtering during schema generation
        if getattr(self, 'swagger_fake_view', False) or not hasattr(self, 'request') or self.request is None:
            return queryset
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by tag
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        
        # Filter by featured
        is_featured = self.request.query_params.get('is_featured', None)
        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured.lower() == 'true')
        
        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(short_title__icontains=search) |
                Q(short_description__icontains=search) |
                Q(content__icontains=search)
            )
        
        # Order by
        ordering = self.request.query_params.get('ordering', '-created_at')
        queryset = queryset.order_by(ordering)
        
        return queryset.distinct()
    
    def list(self, request):
        """List all published blogs with pagination"""
        from rest_framework.pagination import PageNumberPagination
        
        queryset = self.get_queryset()
        
        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(queryset, request)
        
        if page is not None:
            serializer = BlogListSerializer(page, many=True)
            paginated_response = paginator.get_paginated_response(serializer.data)
            
            return create_response(
                status_code=status.HTTP_200_OK,
                message="Blogs retrieved successfully",
                message_code="BLOGS_RETRIEVED",
                data=paginated_response.data.get('results', []),
                count=paginated_response.data.get('count', 0),
                next_link=paginated_response.data.get('next'),
                previous_link=paginated_response.data.get('previous')
            )
        
        serializer = BlogListSerializer(queryset, many=True)
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Blogs retrieved successfully",
            message_code="BLOGS_RETRIEVED",
            data=serializer.data
        )
    
    def retrieve(self, request, pk=None):
        """Retrieve a single blog"""
        try:
            blog = Blog.objects.select_related('author', 'category').prefetch_related('tags').get(pk=pk, status='published')
        except Blog.DoesNotExist:
            return create_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Blog not found",
                message_code="BLOG_NOT_FOUND",
                status=False
            )
        
        # Increment views count
        blog.views_count += 1
        blog.save(update_fields=['views_count'])
        
        serializer = BlogDetailSerializer(blog)
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Blog retrieved successfully",
            message_code="BLOG_RETRIEVED",
            data=serializer.data
        )

    def dynamic_fields(self, request):
        """
        Get dynamic fields for a blog
        ?blog_id=<id>
        """

        blog_id = request.query_params.get('blog_id')

        if not blog_id:
            return create_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="blog_id query parameter is required",
                message_code="BLOG_ID_REQUIRED",
                status=False
            )

        if not Blog.objects.filter(id=blog_id).exists():
            return create_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Blog not found",
                message_code="BLOG_NOT_FOUND",
                status=False
            )

        fields_qs = BlogDynamicField.objects.filter(
            blog_id=blog_id,
            is_active=True
        ).order_by('sequence')

        serializer = BlogDynamicFieldSerializer(fields_qs, many=True)

        return create_response(
            status_code=status.HTTP_200_OK,
            message="Blog dynamic fields retrieved successfully",
            message_code="BLOG_DYNAMIC_FIELDS_RETRIEVED",
            data={
                "blog_id": int(blog_id),
                "total_fields": fields_qs.count(),
                "fields": serializer.data
            }
        )

class BlogLeadsViewSet(viewsets.ViewSet):
    """
    ViewSet for Blog Leads - CREATE operation only
    """
    
    @swagger_auto_schema(
        operation_description="""
        Submit a new case study lead/inquiry.

        **Content Type:** `application/json`

        **Field Requirements:**
        - All fields are optional
        - Recommended: `name` and `email`

        **Lead Source Options:**
        - `download` - Case Study Download
        - `contact` - Contact Form
        - `demo` - Demo Request
        - `consultation` - Consultation Request
        - `newsletter` - Newsletter Signup
        - `other` - Other (default)
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'case_study': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the related case study',
                    example=1
                ),
                'data': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description='Dynamic lead data like name, email, phone, etc.',
                    example={
                        "name": "Jane Smith",
                        "email": "jane.smith@example.com",
                        "phone": "+1234567890",
                        "company": "Tech Corp",
                        "job_title": "Marketing Manager",
                        "lead_source": "download",
                        "message": "I would like to download this case study.",
                        "utm_source": "google",
                        "utm_medium": "cpc",
                        "utm_campaign": "case_study_promo",
                        "utm_refcode": "REF456"
                    }
                )
            },
            required=[]
        ),
        responses={
            201: openapi.Response(
                description='Blog lead created successfully',
                examples={
                    "application/json": {
                        "status": True,
                        "status_code": 201,
                        "message": "Lead created successfully",
                        "message_code": "CASE_STUDY_LEAD_CREATED",
                        "data": {
                            "id": 12,
                            "case_study_id": 1,
                            "data": {
                                "name": "Jane Smith",
                                "email": "jane.smith@example.com"
                            }
                        }
                    }
                }
            ),
            400: openapi.Response(description='Bad request - validation errors')
        },
        tags=['Blog Leads']
    )
    def create(self, request):
        serializer = BlogLeadsCreateSerializer(data=request.data)
        if serializer.is_valid():
            lead = serializer.save()
            return create_response(
                status_code=status.HTTP_201_CREATED,
                message="Lead created successfully",
                message_code="BLOG_LEAD_CREATED",
                data={
                    "id": lead.id,
                    "blog_id": lead.blog.id if lead.blog else None,
                    "data": lead.data
                }
            )
        return create_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Invalid data",
            message_code="INVALID_LEAD_DATA",
            data=serializer.errors,
            status=False
        )