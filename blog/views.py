from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from martech_influence_backend.utils import create_response
from .models import Blog, BlogLeads
from .serializers import (
    BlogListSerializer, BlogDetailSerializer,
    BlogLeadsCreateSerializer
)


class BlogViewSet(viewsets.ViewSet):
    """
    ViewSet for Blog - GET operations only
    """
    
    def get_queryset(self):
        queryset = Blog.objects.select_related('author', 'category').prefetch_related('tags').filter(status='published')
        
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


class BlogLeadsViewSet(viewsets.ViewSet):
    """
    ViewSet for Blog Leads - CREATE operation only
    """
    
    @swagger_auto_schema(
        operation_description="""
        Submit a new blog lead/inquiry.
        
        **Content Type:** `application/json`
        
        **Headers:**
        - `Content-Type: application/json` (Required)
        
        **Field Requirements:**
        - All fields are **optional** (can be null/blank)
        - However, it's recommended to provide at least `name` and `email`
        
        **Lead Source Options:**
        - `newsletter` - Newsletter Signup
        - `download` - Resource Download
        - `contact` - Contact Form
        - `demo` - Demo Request
        - `other` - Other (default)
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],  # All fields are optional
            properties={
                'blog': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='Blog ID (optional) - ID of the blog post related to this lead',
                    example=1
                ),
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Full name of the lead (optional, max 100 characters)',
                    example='John Doe'
                ),
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    description='Email address of the lead (optional)',
                    example='john.doe@example.com'
                ),
                'phone': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Phone number (optional, max 20 characters)',
                    example='+1234567890'
                ),
                'company': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Company name (optional, max 100 characters)',
                    example='Acme Corp'
                ),
                'lead_source': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['newsletter', 'download', 'contact', 'demo', 'other'],
                    description='Source of the lead (optional, default: "other")',
                    example='contact'
                ),
                'message': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Message or inquiry details (optional)',
                    example='I am interested in learning more about this blog post.'
                ),
                'utm_source': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='UTM source parameter for tracking (optional, max 100 characters)',
                    example='google'
                ),
                'utm_medium': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='UTM medium parameter for tracking (optional, max 100 characters)',
                    example='cpc'
                ),
                'utm_campaign': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='UTM campaign parameter for tracking (optional, max 100 characters)',
                    example='summer_sale'
                ),
                'utm_refcode': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='UTM reference code for tracking (optional, max 100 characters)',
                    example='REF123'
                ),
            },
            example={
                'blog': 1,
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '+1234567890',
                'company': 'Acme Corp',
                'lead_source': 'contact',
                'message': 'I am interested in learning more about this blog post.',
                'utm_source': 'google',
                'utm_medium': 'cpc',
                'utm_campaign': 'blog_promotion',
                'utm_refcode': 'REF123'
            }
        ),
        responses={
            201: openapi.Response(
                description='Blog lead created successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, example=201),
                        'message_code': openapi.Schema(type=openapi.TYPE_STRING, example='BLOG_LEAD_CREATED'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, example='Blog Lead Submitted Successfully'),
                        'data': openapi.Schema(type=openapi.TYPE_OBJECT)
                    }
                )
            ),
            400: openapi.Response(
                description='Bad request - validation errors',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, example=400),
                        'message_code': openapi.Schema(type=openapi.TYPE_STRING, example='BLOG_LEAD_CREATION_FAILED'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, example='Blog Lead Submission Failed'),
                        'data': openapi.Schema(type=openapi.TYPE_OBJECT, description='Validation errors')
                    }
                )
            )
        },
        tags=['Blog Leads']
    )
    def create(self, request):
        """Create a new blog lead"""
        serializer = BlogLeadsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return create_response(
                status_code=status.HTTP_201_CREATED,
                message="Blog lead submitted successfully",
                message_code="BLOG_LEAD_CREATED",
                data=serializer.data
            )
        return create_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Blog lead submission failed",
            message_code="BLOG_LEAD_CREATION_FAILED",
            status=False,
            data=serializer.errors
        )
