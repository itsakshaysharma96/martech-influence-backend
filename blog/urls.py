from django.urls import path
from .views import BlogViewSet, BlogLeadsViewSet

blog_list = BlogViewSet.as_view({'get': 'list'})
blog_detail = BlogViewSet.as_view({'get': 'retrieve'})
blog_lead_create = BlogLeadsViewSet.as_view({'post': 'create'})

urlpatterns = [
    path('blogs/', blog_list, name='blog-list'),
    path('blogs/<int:pk>/', blog_detail, name='blog-detail'),
    path('blog-leads/', blog_lead_create, name='blog-lead-create'),
]
