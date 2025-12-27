from django.urls import path
from .views import BlogViewSet, BlogLeadsViewSet

blog_list = BlogViewSet.as_view({'get': 'list'})
blog_detail = BlogViewSet.as_view({'get': 'retrieve'})
blog_lead_create = BlogLeadsViewSet.as_view({'post': 'create'})
blog_dynamic_fields = BlogViewSet.as_view({'get': 'dynamic_fields'}) 

urlpatterns = [
    path('blogs/', blog_list, name='blog-list'),
    path('blogs/<int:pk>/', blog_detail, name='blog-detail'),
    path('blogs/dynamic-fields/', blog_dynamic_fields, name='blog-dynamic-fields'),
    path('blog-leads/', blog_lead_create, name='blog-lead-create'),
]
