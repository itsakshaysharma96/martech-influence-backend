from rest_framework import viewsets, status
from martech_influence_backend.utils import create_response
from .models import SocialMedia
from .serializers import SocialMediaSerializer


class SocialMediaViewSet(viewsets.ViewSet):
    """
    ViewSet for Social Media - GET operations only
    """
    
    def get_queryset(self):
        queryset = SocialMedia.objects.filter(is_active=True)
        
        # Filter by platform
        platform = self.request.query_params.get('platform', None)
        if platform:
            queryset = queryset.filter(platform=platform)
        
        # Order by platform
        queryset = queryset.order_by('platform')
        
        return queryset
    
    def list(self, request):
        """List all active social media links"""
        queryset = self.get_queryset()
        serializer = SocialMediaSerializer(queryset, many=True, context={'request': request})
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Social media links retrieved successfully",
            message_code="SOCIAL_MEDIA_RETRIEVED",
            data=serializer.data
        )
    
    def retrieve(self, request, pk=None):
        """Retrieve a single social media link"""
        try:
            social_media = SocialMedia.objects.get(pk=pk, is_active=True)
        except SocialMedia.DoesNotExist:
            return create_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Social media link not found",
                message_code="SOCIAL_MEDIA_NOT_FOUND",
                status=False
            )
        
        serializer = SocialMediaSerializer(social_media, context={'request': request})
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Social media link retrieved successfully",
            message_code="SOCIAL_MEDIA_RETRIEVED",
            data=serializer.data
        )
