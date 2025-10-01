from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from djoser.serializers import UserCreateSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from apps.users.models import Profile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="profile.gender", read_only=True)
    phone_number = PhoneNumberField(source="profile.phone_number", read_only=True)
    profile_photo = serializers.ImageField(
        source="profile.profile_photo", read_only=True
    )
    country = CountryField(source="profile.country", read_only=True)
    city = serializers.CharField(source="profile.city", read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)

    # Provider application fields
    provider_application_status = serializers.CharField(
        source="profile.provider_application_status", read_only=True
    )
    is_verified_provider = serializers.BooleanField(
        source="profile.is_verified_provider", read_only=True
    )

    class Meta:
        model = User
        fields = [
            "pkid",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "gender",
            "phone_number",
            "profile_photo",
            "country",
            "city",
            "role",
            "is_active",
            "date_joined",
            "provider_application_status",
            "is_verified_provider",
        ]
        read_only_fields = ["pkid", "email", "date_joined"]

    def get_full_name(self, obj):
        return obj.get_fullname

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["admin"] = instance.is_superuser
        return data


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["pkid", "username", "email", "first_name", "last_name", "password"]


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    country = CountryField(name_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    joined_date = serializers.SerializerMethodField(read_only=True)
    last_login = serializers.SerializerMethodField(read_only=True)
    membership_duration = serializers.CharField(
        source="user.membership_duration", read_only=True
    )
    role = serializers.CharField(source="user.role", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "full_name",
            "country",
            "address",
            "about_me",
            "city",
            "gender",
            "phone_number",
            "profile_photo",
            "joined_date",
            "last_login",
            "membership_duration",
            "role",
            # Provider fields
            "is_verified_provider",
            "business_name",
            "business_address",
            "latitude",
            "longitude",
            "description",
            "subscription_tier",
            "subscription_expires_at",
            # Provider application fields
            "provider_application_status",
            "provider_application_date",
            "withdrawn_date",
            "provider_application_data",
            "years_of_experience",
            "certifications",
            "portfolio_urls",
            "service_categories",
            "availability_schedule",
            "emergency_contact",
            # Client fields
            "loyalty_points",
        ]

    def get_full_name(self, obj):
        return obj.user.get_fullname

    def get_joined_date(self, obj):
        return obj.joined_date

    def get_last_login(self, obj):
        return obj.last_login


class UpdateProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    # Allow updating user fields through profile
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)

    class Meta:
        model = Profile
        fields = [
            # User fields
            "first_name",
            "last_name",
            # Basic profile fields
            "phone_number",
            "profile_photo",
            "about_me",
            "gender",
            "country",
            "city",
            "address",
            # Provider business fields
            "business_name",
            "business_address",
            "latitude",
            "longitude",
            "description",
            # Additional provider details
            "years_of_experience",
            "certifications",
            "portfolio_urls",
            "service_categories",
            "availability_schedule",
            "emergency_contact",
        ]

    def update(self, instance, validated_data):
        # Handle user data if present
        user_data = validated_data.pop("user", {})
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        # Update profile data
        return super().update(instance, validated_data)


class ProviderApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer specifically for provider applications
    """

    class Meta:
        model = Profile
        fields = [
            "business_name",
            "business_address",
            "description",
            "latitude",
            "longitude",
            "years_of_experience",
            "certifications",
            "portfolio_urls",
            "service_categories",
            "availability_schedule",
            "emergency_contact",
        ]


class UnifiedProfileSerializer(serializers.ModelSerializer):
    # Profile fields
    about_me = serializers.CharField(source="profile.about_me", read_only=True)
    profile_photo = serializers.ImageField(
        source="profile.profile_photo", read_only=True
    )
    gender = serializers.CharField(source="profile.gender", read_only=True)
    country = CountryField(source="profile.country", read_only=True)
    city = serializers.CharField(source="profile.city", read_only=True)
    address = serializers.CharField(source="profile.address", read_only=True)

    # Provider fields
    business_name = serializers.CharField(
        source="profile.business_name", read_only=True
    )
    business_address = serializers.CharField(
        source="profile.business_address", read_only=True
    )
    latitude = serializers.DecimalField(
        source="profile.latitude", read_only=True, max_digits=10, decimal_places=8
    )
    longitude = serializers.DecimalField(
        source="profile.longitude", read_only=True, max_digits=11, decimal_places=8
    )
    is_verified_provider = serializers.BooleanField(
        source="profile.is_verified_provider", read_only=True
    )
    description = serializers.CharField(source="profile.description", read_only=True)
    subscription_tier = serializers.CharField(
        source="profile.subscription_tier", read_only=True
    )
    subscription_expires_at = serializers.DateTimeField(
        source="profile.subscription_expires_at", read_only=True
    )

    # Provider application fields
    provider_application_status = serializers.CharField(
        source="profile.provider_application_status", read_only=True
    )
    provider_application_date = serializers.DateTimeField(
        source="profile.provider_application_date", read_only=True
    )
    provider_application_data = serializers.JSONField(
        source="profile.provider_application_data", read_only=True
    )
    years_of_experience = serializers.IntegerField(
        source="profile.years_of_experience", read_only=True
    )
    certifications = serializers.JSONField(
        source="profile.certifications", read_only=True
    )
    portfolio_urls = serializers.JSONField(
        source="profile.portfolio_urls", read_only=True
    )
    service_categories = serializers.JSONField(
        source="profile.service_categories", read_only=True
    )
    availability_schedule = serializers.CharField(
        source="profile.availability_schedule", read_only=True
    )
    emergency_contact = serializers.CharField(
        source="profile.emergency_contact", read_only=True
    )

    # Client fields
    loyalty_points = serializers.IntegerField(
        source="profile.loyalty_points", read_only=True
    )
    phone_number = PhoneNumberField(source="profile.phone_number", read_only=True)

    # Computed fields
    full_name = serializers.SerializerMethodField(read_only=True)
    membership_duration = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "pkid",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "is_active",
            "date_joined",
            # Basic profile fields
            "phone_number",
            "about_me",
            "profile_photo",
            "gender",
            "country",
            "city",
            "address",
            # Provider business fields
            "business_name",
            "business_address",
            "latitude",
            "longitude",
            "is_verified_provider",
            "description",
            "subscription_tier",
            "subscription_expires_at",
            # Provider application fields
            "provider_application_status",
            "provider_application_date",
            "provider_application_data",
            "years_of_experience",
            "certifications",
            "portfolio_urls",
            "service_categories",
            "availability_schedule",
            "emergency_contact",
            # Client fields
            "loyalty_points",
            "membership_duration",
        ]
        read_only_fields = ["pkid", "email", "date_joined"]

    def get_full_name(self, obj):
        return obj.get_fullname

    def get_membership_duration(self, obj):
        return obj.membership_duration


class ProviderApplicationStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for provider application status
    """

    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "provider_application_status",
            "provider_application_date",
            "withdrawn_date",
            "is_verified_provider",
            "business_name",
            "username",
            "email",
        ]
