# apps/services/views.py
import logging
from django.db.models import Count, Avg, Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import ServiceCategory, Service
from .serializers import (
    ServiceCategorySerializer,
    ServiceCategoryCreateSerializer,
    ServiceSerializer,
    ServiceCreateSerializer,
    ServiceUpdateSerializer,
    ServiceDetailSerializer,
    ProviderServiceStatsSerializer,
)

logger = logging.getLogger(__name__)


# Service Category Views
@swagger_auto_schema(
    method="GET",
    operation_description="Get all service categories",
    responses={200: ServiceCategorySerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_categories(request):
    """Get all active service categories"""
    categories = ServiceCategory.objects.filter(is_active=True)
    serializer = ServiceCategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="GET",
    operation_description="Get service category by ID",
    responses={200: ServiceCategorySerializer, 404: "Category not found"},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_category_detail(request, category_id):
    """Get specific service category details"""
    category = get_object_or_404(ServiceCategory, id=category_id, is_active=True)
    serializer = ServiceCategorySerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="POST",
    operation_description="Create new service category (Admin only)",
    request_body=ServiceCategoryCreateSerializer,
    responses={201: ServiceCategorySerializer, 400: "Bad request", 403: "Forbidden"},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_category(request):
    """Create new service category (Admin only)"""
    if not request.user.is_staff and not request.user.is_superuser:
        return Response(
            {"error": "Only admin users can create categories"},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = ServiceCategoryCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="PUT",
    operation_description="Update service category (Admin only)",
    request_body=ServiceCategoryCreateSerializer,
    responses={
        200: ServiceCategorySerializer,
        400: "Bad request",
        403: "Forbidden",
        404: "Not found",
    },
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_category(request, category_id):
    """Update service category (Admin only)"""
    if not request.user.is_staff and not request.user.is_superuser:
        return Response(
            {"error": "Only admin users can update categories"},
            status=status.HTTP_403_FORBIDDEN,
        )

    category = get_object_or_404(ServiceCategory, id=category_id)
    serializer = ServiceCategoryCreateSerializer(category, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="DELETE",
    operation_description="Delete service category (Admin only)",
    responses={204: "No content", 403: "Forbidden", 404: "Not found"},
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_category(request, category_id):
    """Delete service category (Admin only)"""
    if not request.user.is_staff and not request.user.is_superuser:
        return Response(
            {"error": "Only admin users can delete categories"},
            status=status.HTTP_403_FORBIDDEN,
        )

    category = get_object_or_404(ServiceCategory, id=category_id)
    category.delete()

    return Response(
        {"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT
    )


# Service Views
@swagger_auto_schema(
    method="GET",
    operation_description="Get all services with filtering options",
    manual_parameters=[
        openapi.Parameter(
            "category",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Filter by category ID",
        ),
        openapi.Parameter(
            "provider",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Filter by provider ID",
        ),
        openapi.Parameter(
            "min_price",
            openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description="Minimum price",
        ),
        openapi.Parameter(
            "max_price",
            openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description="Maximum price",
        ),
        openapi.Parameter(
            "search",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Search in name and description",
        ),
        openapi.Parameter(
            "verified_only",
            openapi.IN_QUERY,
            type=openapi.TYPE_BOOLEAN,
            description="Only verified providers",
        ),
    ],
    responses={200: ServiceSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_services(request):
    """Get all active services with optional filtering"""
    services = Service.objects.filter(is_active=True)

    # Apply filters
    category_id = request.GET.get("category")
    if category_id:
        services = services.filter(category_id=category_id)

    provider_id = request.GET.get("provider")
    if provider_id:
        services = services.filter(provider_id=provider_id)

    min_price = request.GET.get("min_price")
    if min_price:
        services = services.filter(price__gte=min_price)

    max_price = request.GET.get("max_price")
    if max_price:
        services = services.filter(price__lte=max_price)

    search = request.GET.get("search")
    if search:
        services = services.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    verified_only = request.GET.get("verified_only")
    if verified_only and verified_only.lower() == "true":
        services = services.filter(provider__is_verified_provider=True)

    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="GET",
    operation_description="Get service by ID",
    responses={200: ServiceDetailSerializer, 404: "Service not found"},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_service_detail(request, service_id):
    """Get specific service details"""
    service = get_object_or_404(Service, id=service_id, is_active=True)
    serializer = ServiceDetailSerializer(service)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="POST",
    operation_description="Create new service (Provider only)",
    request_body=ServiceCreateSerializer,
    responses={201: ServiceSerializer, 400: "Bad request", 403: "Forbidden"},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_service(request):
    """Create new service (Provider only)"""
    if request.user.role != "provider":
        return Response(
            {"error": "Only providers can create services"},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = ServiceCreateSerializer(
        data=request.data, context={"request": request}
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="PUT",
    operation_description="Update service (Provider only - must own the service)",
    request_body=ServiceUpdateSerializer,
    responses={
        200: ServiceSerializer,
        400: "Bad request",
        403: "Forbidden",
        404: "Not found",
    },
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_service(request, service_id):
    """Update service (Provider only - must own the service)"""
    service = get_object_or_404(Service, id=service_id)

    # Check if user owns this service
    if service.provider.user != request.user:
        return Response(
            {"error": "You can only update your own services"},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = ServiceUpdateSerializer(service, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="DELETE",
    operation_description="Delete service (Provider only - must own the service)",
    responses={204: "No content", 403: "Forbidden", 404: "Not found"},
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_service(request, service_id):
    """Delete service (Provider only - must own the service)"""
    service = get_object_or_404(Service, id=service_id)

    # Check if user owns this service
    if service.provider.user != request.user:
        return Response(
            {"error": "You can only delete your own services"},
            status=status.HTTP_403_FORBIDDEN,
        )

    service.delete()

    return Response(
        {"message": "Service deleted successfully"}, status=status.HTTP_204_NO_CONTENT
    )


@swagger_auto_schema(
    method="GET",
    operation_description="Get current provider's services",
    responses={200: ServiceSerializer(many=True), 403: "Forbidden"},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_services(request):
    """Get current provider's services"""
    if request.user.role != "provider":
        return Response(
            {"error": "Only providers can access this endpoint"},
            status=status.HTTP_403_FORBIDDEN,
        )

    services = Service.objects.filter(provider=request.user.profile)
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="GET",
    operation_description="Get provider service statistics",
    responses={200: ProviderServiceStatsSerializer, 403: "Forbidden"},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_service_stats(request):
    """Get current provider's service statistics"""
    if request.user.role != "provider":
        return Response(
            {"error": "Only providers can access this endpoint"},
            status=status.HTTP_403_FORBIDDEN,
        )

    provider_profile = request.user.profile
    services = Service.objects.filter(provider=provider_profile)

    stats = {
        "total_services": services.count(),
        "active_services": services.filter(is_active=True).count(),
        "inactive_services": services.filter(is_active=False).count(),
        "total_categories": services.values("category").distinct().count(),
        "average_price": services.aggregate(avg_price=Avg("price"))["avg_price"] or 0,
    }

    serializer = ProviderServiceStatsSerializer(stats)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="GET",
    operation_description="Get services by provider ID",
    responses={200: ServiceSerializer(many=True), 404: "Provider not found"},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_provider_services(request, provider_id):
    """Get all services for a specific provider"""
    services = Service.objects.filter(provider_id=provider_id, is_active=True)

    if not services.exists():
        return Response(
            {"error": "No services found for this provider"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="GET",
    operation_description="Get services by category ID",
    responses={200: ServiceSerializer(many=True), 404: "Category not found"},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_category_services(request, category_id):
    """Get all services for a specific category"""
    category = get_object_or_404(ServiceCategory, id=category_id, is_active=True)
    services = Service.objects.filter(category=category, is_active=True)

    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
