from django.urls import path
from .views import SocialMediaViewSet

social_media_list = SocialMediaViewSet.as_view({'get': 'list'})
social_media_detail = SocialMediaViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
    path('social-media/', social_media_list, name='social-media-list'),
    path('social-media/<int:pk>/', social_media_detail, name='social-media-detail'),
]

