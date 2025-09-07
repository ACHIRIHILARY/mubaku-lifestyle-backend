from django.urls import path
from . import controllers

app_name = "users_api"

urlpatterns = [
    # Current user endpoints
    path("me/", controllers.get_current_user_profile, name="my_profile"),
    path("me/data/", controllers.get_current_user_data, name="current_user_data"),
    path("me/unified/", controllers.unified_profile_view, name="unified_profile"),
    # Role management
    path("update-role/", controllers.update_user_role, name="update_user_role"),
    # Profile management by username
    path(
        "<str:username>/",
        controllers.get_profile_by_username,
        name="get_profile_by_username",
    ),
    path("<str:username>/update/", controllers.update_profile, name="update_profile"),
    # Admin actions
    path(
        "<str:username>/verify-provider/",
        controllers.verify_provider,
        name="verify_provider",
    ),
]
