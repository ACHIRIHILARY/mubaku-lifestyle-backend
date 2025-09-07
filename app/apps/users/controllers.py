import logging
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .exceptions import NotYourProfileException, ProfileNotFoundException
from apps.users.models import Profile, User
from .renderers import ProfileJSONRenderer
from .serializers import (
    ProfileSerializer,
    UpdateProfileSerializer,
    UnifiedProfileSerializer,
    UserSerializer,
)

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method="GET",
    operation_description="Get current user's profile",
    responses={200: ProfileSerializer},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_user_profile(request):
    """
    Get the current authenticated user's profile
    """
    try:
        user_profile = request.user.profile
        serializer = ProfileSerializer(user_profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        raise ProfileNotFoundException("Profile does not exist for this user")


@swagger_auto_schema(
    method="GET",
    operation_description="Get user profile by username",
    responses={200: ProfileSerializer, 403: "Forbidden", 404: "Not Found"},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile_by_username(request, username):
    """
    Get a specific user's profile by username
    """
    try:
        profile = Profile.objects.get(user__username=username)

        if not (
            request.user.is_staff
            or request.user.is_superuser
            or request.user.username == username
        ):
            return Response(
                {"error": "You don't have permission to view this profile"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProfileSerializer(profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        raise ProfileNotFoundException("Profile does not exist")


@swagger_auto_schema(
    method="PATCH",
    operation_description="Update user profile",
    request_body=UpdateProfileSerializer,
    responses={
        200: ProfileSerializer,
        400: "Bad Request",
        403: "Forbidden",
        404: "Not Found",
    },
)
@swagger_auto_schema(
    method="PUT",
    operation_description="Update user profile (full update)",
    request_body=UpdateProfileSerializer,
    responses={
        200: ProfileSerializer,
        400: "Bad Request",
        403: "Forbidden",
        404: "Not Found",
    },
)
@api_view(["PATCH", "PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request, username):
    """
    Update a user's profile - only allowed for the profile owner
    """
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        raise ProfileNotFoundException("Profile does not exist")

    if request.user.username != username and not request.user.is_superuser:
        raise NotYourProfileException("Not your profile to update")

    if request.method in ["PATCH", "PUT"]:
        serializer = UpdateProfileSerializer(
            instance=profile, data=request.data, partial=(request.method == "PATCH")
        )

        if serializer.is_valid():
            serializer.save()

            updated_profile = Profile.objects.get(user__username=username)
            response_serializer = ProfileSerializer(
                updated_profile, context={"request": request}
            )
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Define the request body schema for role update
role_update_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["role"],
    properties={
        "role": openapi.Schema(
            type=openapi.TYPE_STRING,
            enum=["client", "provider", "admin", "superuser"],
            description="User role",
        )
    },
)


@swagger_auto_schema(
    method="POST",
    operation_description="Update user role",
    request_body=role_update_schema,
    responses={
        200: openapi.Response(
            description="Role updated successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING),
                    "role": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        ),
        400: "Bad Request",
        403: "Forbidden",
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_user_role(request):
    """
    Update the role of the authenticated user
    """
    valid_roles = ["client", "provider", "admin", "superuser"]
    user = request.user
    new_role = request.data.get("role")

    if not new_role:
        return Response(
            {"error": "Role must be provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    if new_role not in valid_roles:
        return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

    if new_role == "superuser" and not user.is_superuser:
        return Response(
            {"error": "Only superusers can assign superuser role"},
            status=status.HTTP_403_FORBIDDEN,
        )

    user.role = new_role
    user.save()

    return Response(
        {"message": "Role updated successfully", "role": user.role},
        status=status.HTTP_200_OK,
    )


# Define the request body schema for unified profile update
unified_profile_update_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "first_name": openapi.Schema(
            type=openapi.TYPE_STRING, description="First name"
        ),
        "last_name": openapi.Schema(type=openapi.TYPE_STRING, description="Last name"),
        "username": openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
        "phone_number": openapi.Schema(
            type=openapi.TYPE_STRING, description="Phone number"
        ),
        "about_me": openapi.Schema(type=openapi.TYPE_STRING, description="About me"),
        "gender": openapi.Schema(type=openapi.TYPE_STRING, description="Gender"),
        "country": openapi.Schema(type=openapi.TYPE_STRING, description="Country"),
        "city": openapi.Schema(type=openapi.TYPE_STRING, description="City"),
        "address": openapi.Schema(type=openapi.TYPE_STRING, description="Address"),
        "profile_photo": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_BINARY,
            description="Profile photo",
        ),
    },
)


@swagger_auto_schema(
    method="GET",
    operation_description="Get unified profile data",
    responses={200: UnifiedProfileSerializer},
)
@swagger_auto_schema(
    method="PUT",
    operation_description="Update unified profile (full update)",
    request_body=unified_profile_update_schema,
    responses={200: UnifiedProfileSerializer, 400: "Bad Request"},
)
@swagger_auto_schema(
    method="PATCH",
    operation_description="Update unified profile (partial update)",
    request_body=unified_profile_update_schema,
    responses={200: UnifiedProfileSerializer, 400: "Bad Request"},
)
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
        user_data = {
            "first_name": request.data.get("first_name", user.first_name),
            "last_name": request.data.get("last_name", user.last_name),
            "username": request.data.get("username", user.username),
        }

        user_serializer = UserSerializer(
            user,
            data=user_data,
            partial=(request.method == "PATCH"),
            context={"request": request},
        )

        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer.save()

        profile_data = {
            "phone_number": request.data.get("phone_number", user.profile.phone_number),
            "about_me": request.data.get("about_me", user.profile.about_me),
            "gender": request.data.get("gender", user.profile.gender),
            "country": request.data.get("country", user.profile.country),
            "city": request.data.get("city", user.profile.city),
            "address": request.data.get("address", user.profile.address),
        }

        if "profile_photo" in request.data:
            profile_data["profile_photo"] = request.data["profile_photo"]

        profile_serializer = UpdateProfileSerializer(
            user.profile,
            data=profile_data,
            partial=(request.method == "PATCH"),
            context={"request": request},
        )

        if not profile_serializer.is_valid():
            return Response(
                profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        profile_serializer.save()

        unified_serializer = UnifiedProfileSerializer(
            user, context={"request": request}
        )
        return Response(unified_serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="GET",
    operation_description="Get current user data",
    responses={200: UserSerializer},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_user_data(request):
    """
    Get current user data (without profile details)
    """
    serializer = UserSerializer(request.user, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="POST",
    operation_description="Verify a provider (admin only)",
    responses={
        200: openapi.Response(
            description="Provider verified successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING),
                    "profile": ProfileSerializer,
                },
            ),
        ),
        403: "Forbidden",
        404: "Not Found",
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_provider(request, username):
    """
    Verify a provider profile (admin only)
    """
    if not request.user.is_staff and not request.user.is_superuser:
        return Response(
            {"error": "Only admin users can verify providers"},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        profile = Profile.objects.get(user__username=username)

        if profile.user.role != "provider":
            return Response(
                {"error": "User is not a provider"}, status=status.HTTP_400_BAD_REQUEST
            )

        profile.is_verified_provider = True
        profile.save()

        serializer = ProfileSerializer(profile, context={"request": request})
        return Response(
            {"message": "Provider verified successfully", "profile": serializer.data},
            status=status.HTTP_200_OK,
        )

    except Profile.DoesNotExist:
        raise ProfileNotFoundException("Profile does not exist")
