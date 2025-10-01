# apps/services/urls.py
from django.urls import path
from . import controllers

app_name = "services"

urlpatterns = [
    # Service Category endpoints
    path("categories/", controllers.get_all_categories, name="category-list"),
    path("categories/create/", controllers.create_category, name="category-create"),
    path(
        "categories/<uuid:category_id>/",
        controllers.get_category_detail,
        name="category-detail",
    ),
    path(
        "categories/<uuid:category_id>/update/",
        controllers.update_category,
        name="category-update",
    ),
    path(
        "categories/<uuid:category_id>/delete/",
        controllers.delete_category,
        name="category-delete",
    ),
    path(
        "categories/<uuid:category_id>/services/",
        controllers.get_category_services,
        name="category-services",
    ),
    # Service endpoints
    path("", controllers.get_all_services, name="service-list"),
    path("create/", controllers.create_service, name="service-create"),
    path("<uuid:service_id>/", controllers.get_service_detail, name="service-detail"),
    path(
        "<uuid:service_id>/update/", controllers.update_service, name="service-update"
    ),
    path(
        "<uuid:service_id>/delete/", controllers.delete_service, name="service-delete"
    ),
    # Provider-specific endpoints
    path("my-services/", controllers.get_my_services, name="my-services"),
    path("my-stats/", controllers.get_my_service_stats, name="my-stats"),
    path(
        "provider/<uuid:provider_id>/",
        controllers.get_provider_services,
        name="provider-services",
    ),
]
