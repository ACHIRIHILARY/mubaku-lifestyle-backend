import logging
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


from .exceptions import NotYourProfileException, ProfileNotFoundException
from apps.users.models import Profile, User
from .serializers import (
    ProfileSerializer,
    UpdateProfileSerializer,
    UnifiedProfileSerializer,
    UserSerializer,
    ProviderApplicationSerializer,
    ProviderApplicationStatusSerializer,
)

logger = logging.getLogger(__name__)


# Helper functions
def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_application_status_message(status, is_verified):
    """Get human-readable application status message"""
    status_messages = {
        "pending": "Your application is under review. We'll notify you once processed.",
        "approved": "Congratulations! Your application has been approved."
        + (
            " Your profile is now verified!"
            if is_verified
            else " Verification pending."
        ),
        "rejected": "We're sorry, your application wasn't approved at this time. Contact support for details.",
        "withdrawn": "You have withdrawn your application.",
        "not_submitted": "No application found. Submit a provider application to get started.",
    }
    return status_messages.get(status, "Unknown application status.")


# Profile Views


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_user_profile(request):
    """Get the current authenticated user's profile"""
    try:
        user_profile = request.user.profile
        serializer = ProfileSerializer(user_profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        raise ProfileNotFoundException("Profile does not exist for this user")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile_by_id(request, id):
    """Get a specific user's profile by ID"""
    try:
        profile = Profile.objects.get(user__id=id)

        if not (
            request.user.is_staff or request.user.is_superuser or request.user.id == id
        ):
            return Response(
                {"error": "You don't have permission to view this profile"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProfileSerializer(profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        raise ProfileNotFoundException("Profile does not exist")


@api_view(["PATCH", "PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request, id):
    """Update a user's profile - only allowed for the profile owner"""
    try:
        profile = Profile.objects.get(user__id=id)
    except Profile.DoesNotExist:
        raise ProfileNotFoundException("Profile does not exist")

    if request.user.id != id and not request.user.is_superuser:
        raise NotYourProfileException("Not your profile to update")

    serializer = UpdateProfileSerializer(
        instance=profile,
        data=request.data,
        partial=(request.method == "PATCH"),
        context={"request": request},
    )

    if serializer.is_valid():
        serializer.save()

        # Return updated profile
        updated_profile = Profile.objects.get(user__id=id)
        response_serializer = ProfileSerializer(
            updated_profile, context={"request": request}
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Role Management Views
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_user_role(request, user_id):
    """Update user role by user ID - only allowed for admin users"""
    # Check if current user has admin privileges
    if (
        request.user.role not in ["admin", "superuser"]
        and not request.user.is_superuser
    ):
        return Response(
            {"error": "Only admin users can update roles"},
            status=status.HTTP_403_FORBIDDEN,
        )

    valid_roles = ["client", "provider", "admin", "superuser"]
    new_role = request.data.get("role")

    if not new_role:
        return Response(
            {"error": "Role must be provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    if new_role not in valid_roles:
        return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

    # Prevent users from modifying their own role (except admins)
    if str(request.user.id) == str(user_id) and request.user.role != "admin":
        return Response(
            {"error": "You cannot modify your own role"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Only superusers can assign superuser role
    if new_role == "superuser" and not request.user.is_superuser:
        return Response(
            {"error": "Only superusers can assign superuser role"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Prevent non-superusers from modifying other admin/superuser roles
    if not request.user.is_superuser:
        if target_user.role in ["admin", "superuser"] or target_user.is_superuser:
            return Response(
                {"error": "You cannot modify other admin users' roles"},
                status=status.HTTP_403_FORBIDDEN,
            )

    # Update the role
    old_role = target_user.role
    target_user.role = new_role
    target_user.save()

    logger.info(
        f"User {request.user.username} ({request.user.role}) changed "
        f"user {target_user.username}'s role from {old_role} to {new_role}"
    )

    return Response(
        {
            "message": "Role updated successfully",
            "user_id": str(target_user.id),
            "username": target_user.username,
            "old_role": old_role,
            "new_role": target_user.role,
        },
        status=status.HTTP_200_OK,
    )


# Unified Profile View


@api_view(["GET", "PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def unified_profile_view(request):
    """
    Unified profile view for GET and UPDATE operations
    GET: Return current user's unified profile data
    PUT/PATCH: Update user and profile information
    """
    user = request.user

    if request.method == "GET":
        serializer = UnifiedProfileSerializer(user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method in ["PUT", "PATCH"]:
        # Use UpdateProfileSerializer for updates
        profile_serializer = UpdateProfileSerializer(
            user.profile,
            data=request.data,
            partial=(request.method == "PATCH"),
            context={"request": request},
        )

        if not profile_serializer.is_valid():
            return Response(
                profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        profile_serializer.save()

        # Return updated unified data
        unified_serializer = UnifiedProfileSerializer(
            user, context={"request": request}
        )
        return Response(unified_serializer.data, status=status.HTTP_200_OK)


# Provider Application Views
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def apply_for_provider(request):
    """Apply to become a service provider on the platform"""
    user = request.user

    # Check if user is already a provider
    if user.role == "provider":
        return Response(
            {
                "error": "You are already a provider",
                "current_status": "active_provider",
            },
            status=status.HTTP_409_CONFLICT,
        )

    # Check if user has a pending application
    if (
        hasattr(user, "profile")
        and user.profile.provider_application_status == "pending"
    ):
        return Response(
            {
                "error": "You already have a pending provider application",
                "application_status": "pending",
                "submitted_date": (
                    user.profile.provider_application_date.isoformat()
                    if user.profile.provider_application_date
                    else None
                ),
            },
            status=status.HTTP_409_CONFLICT,
        )

    # Validate input using serializer
    serializer = ProviderApplicationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {"error": "Invalid application data", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        with transaction.atomic():
            # Update user role to provider (unverified)
            old_role = user.role
            user.role = "provider"
            user.save()

            # Update profile with provider-specific information
            profile = user.profile

            # Update fields from validated data
            for field, value in serializer.validated_data.items():
                setattr(profile, field, value)

            # Set application metadata
            profile.provider_application_status = "pending"
            profile.provider_application_date = timezone.now()
            profile.is_verified_provider = False  # Start as unverified

            # Store application metadata in JSON field
            application_metadata = {
                "applied_from_ip": get_client_ip(request),
                "applied_at": timezone.now().isoformat(),
                "previous_role": old_role,
            }

            profile.provider_application_data = application_metadata
            profile.save()

            # Log the application
            logger.info(
                f"Provider application submitted: User {user.username} ({user.id}) "
                f"from {old_role} to provider. Business: {profile.business_name}"
            )

        # Prepare success response
        response_data = {
            "message": "Provider application submitted successfully!",
            "application_id": f"PROV-APP-{user.id}-{int(timezone.now().timestamp())}",
            "estimated_review_time": "24-48 hours",
            "next_steps": [
                "Our team will review your application",
                "You'll receive an email notification once processed",
                "Check your dashboard for application status updates",
                "Prepare your service offerings while you wait",
            ],
            "application_details": {
                "business_name": profile.business_name,
                "application_date": profile.provider_application_date.isoformat(),
                "current_status": "under_review",
                "contact_email": user.email,
            },
            "tips": [
                "Complete your service portfolio while waiting",
                "Upload professional photos of your previous work",
                "Prepare your pricing strategy",
                "Review our provider guidelines",
            ],
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(
            f"Error submitting provider application for user {user.id}: {str(e)}"
        )
        return Response(
            {
                "error": "Application submission failed",
                "details": "Please try again or contact support if the problem persists",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_provider_application_status(request):
    """Check the status of your provider application"""
    user = request.user

    if not hasattr(user, "profile"):
        return Response(
            {"error": "No profile found", "suggestion": "Complete your profile first"},
            status=status.HTTP_404_NOT_FOUND,
        )

    profile = user.profile

    # If user is not a provider and has no application, return not found
    if user.role != "provider" and profile.provider_application_status != "pending":
        return Response(
            {
                "error": "No provider application found",
                "suggestion": "Submit a provider application first",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = ProviderApplicationStatusSerializer(
        profile, context={"request": request}
    )

    # Add additional info based on status
    response_data = serializer.data
    response_data["message"] = get_application_status_message(
        profile.provider_application_status, profile.is_verified_provider
    )

    if (
        profile.provider_application_status == "approved"
        and profile.is_verified_provider
    ):
        response_data["congratulations"] = "Welcome to our provider network! 🎉"
        response_data["next_steps"] = [
            "Complete your service listings",
            "Set up your availability calendar",
            "Start accepting booking requests",
        ]
    elif profile.provider_application_status == "rejected":
        response_data["contact_support"] = True
        response_data["support_email"] = "providers@mubaku.com"

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def withdraw_provider_application(request):
    """Withdraw your pending provider application"""
    user = request.user

    if not hasattr(user, "profile"):
        return Response(
            {"error": "No profile found"}, status=status.HTTP_400_BAD_REQUEST
        )

    profile = user.profile
    application_status = profile.provider_application_status

    if application_status != "pending":
        return Response(
            {
                "error": "Cannot withdraw application",
                "reason": f"Application status is '{application_status}', only pending applications can be withdrawn",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Revert to client role and update application status
    user.role = "client"
    user.save()

    profile.provider_application_status = "withdrawn"
    profile.withdrawn_date = timezone.now()
    profile.save()

    logger.info(f"Provider application withdrawn by user {user.username}")

    return Response(
        {
            "message": "Provider application withdrawn successfully",
            "previous_status": application_status,
            "current_role": user.role,
            "note": "You can reapply anytime with updated information",
        },
        status=status.HTTP_200_OK,
    )


# Admin Views


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_provider(request, id):
    """Verify a provider profile (admin only)"""
    if not request.user.is_staff and not request.user.is_superuser:
        return Response(
            {"error": "Only admin users can verify providers"},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        profile = Profile.objects.get(user__id=id)

        if profile.user.role != "provider":
            return Response(
                {"error": "User is not a provider"}, status=status.HTTP_400_BAD_REQUEST
            )

        profile.is_verified_provider = True
        profile.provider_application_status = "approved"
        profile.save()

        serializer = ProfileSerializer(profile, context={"request": request})
        return Response(
            {"message": "Provider verified successfully", "profile": serializer.data},
            status=status.HTTP_200_OK,
        )

    except Profile.DoesNotExist:
        raise ProfileNotFoundException("Profile does not exist")


# Utility Views


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_user_data(request):
    """Get current user data (without profile details)"""
    serializer = UserSerializer(request.user, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)
