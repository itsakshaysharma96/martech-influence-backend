"""
URL configuration for martech_influence_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="Martech Influence Backend API",
        default_version='v1',
        description="""
        Complete API documentation for Martech Influence Backend.
        
        ## Features
        - **Blog**: Blog posts, categories, tags, and lead management
        - **Case Study**: Case studies with client information and lead tracking
        - **Career**: Job postings, applications, departments, and locations
        - **Contact**: Contact form submissions with UTM tracking
        - **Social Media**: Dynamic social media links management
        - **Services**: Service listings, categories, and inquiry management
        
        ## Authentication
        Currently, the API does not require authentication for public endpoints.
        Admin endpoints require Django admin authentication.
        
        ## Response Format
        All API responses follow a standardized format:
        ```json
        {
            "status": true,
            "status_code": 200,
            "message_code": "SUCCESS",
            "message": "Operation Successful",
            "data": {...},
            "count": 10,
            "next": "...",
            "previous": "..."
        }
        ```
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@martechinfluence.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # TinyMCE
    path('tinymce/', include('tinymce.urls')),
    
    # API Documentation (Swagger/OpenAPI)
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api-docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),  # Alias for swagger
    
    # API URLs
    path('api/blog/', include('blog.urls')),
    path('api/casestudy/', include('casestudy.urls')),
    path('api/career/', include('career.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/social-media/', include('socialmedia.urls')),
    path('api/services/', include('services.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
