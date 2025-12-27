from django.shortcuts import render
from privacy_policy.models import PrivacyPolicy
from privacy_policy.serializers import PrivacyPolicySerializer
from martech_influence_backend.utils import create_response
from rest_framework import viewsets, status


class PrivacyPolicyViewSet(viewsets.ViewSet):
    """
    API to fetch active Privacy Policy
    """

    def list(self, request):
        """
        GET /api/privacy-policy/
        Returns latest active privacy policy
        """
        policy = PrivacyPolicy.objects.filter(
            is_active=True
        ).order_by("-published_at").first()

        if not policy:
            return create_response(
                success=False,
                message="No active privacy policy found.",
                status_code=status.HTTP_404_NOT_FOUND
            )
            
        serializer = PrivacyPolicySerializer(policy)
        return create_response(
            message_code="PRIVACY_POLICY_FETCHED",
            message="Privacy policy fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )