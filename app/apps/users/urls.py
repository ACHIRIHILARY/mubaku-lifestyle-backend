from django.urls import path
from . import controllers

app_name = "users_api"

urlpatterns = [
    # Current user endpoints
    path("me/", controllers.get_current_user_profile, name="my_profile"),
    path("me/data/", controllers.get_current_user_data, name="current_user_data"),
    path("me/unified/", controllers.unified_profile_view, name="unified_profile"),
    # Role management
    path(
        "<uuid:user_id>/update-role/",
        controllers.update_user_role,
        name="update_user_role",
    ),
    # Profile management by id
    path(
        "<uuid:id>/",
        controllers.get_profile_by_id,
        name="get_profile_by_id",
    ),
    path("<uuid:id>/update/", controllers.update_profile, name="update_profile"),
    # Admin actions
    path(
        "<uuid:id>/verify-provider/",
        controllers.verify_provider,
        name="verify_provider",
    ),
    # Provider application
    path("apply-provider/", controllers.apply_for_provider, name="apply_provider"),
    path(
        "application-status/",
        controllers.check_provider_application_status,
        name="application_status",
    ),
    path(
        "withdraw-application/",
        controllers.withdraw_provider_application,
        name="withdraw_application",
    ),
]
