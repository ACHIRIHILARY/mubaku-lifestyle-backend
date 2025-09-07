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
            "is_verified_provider",
            "business_name",
            "business_address",
            "latitude",
            "longitude",
            "description",
            "subscription_tier",
            "subscription_expires_at",
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
            "first_name",
            "last_name",
            "phone_number",
            "profile_photo",
            "about_me",
            "gender",
            "country",
            "city",
            "address",
            "business_name",
            "business_address",
            "latitude",
            "longitude",
            "description",
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

    # Client fields
    loyalty_points = serializers.IntegerField(
        source="profile.loyalty_points", read_only=True
    )
    phone_number = PhoneNumberField(source="profile.phone_number", read_only=True)

    # Computed fields
    full_name = serializers.SerializerMethodField(read_only=True)
    membership_duration = serializers.CharField(
        source="membership_duration", read_only=True
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
            "role",
            "is_active",
            "date_joined",
            "phone_number",
            "about_me",
            "profile_photo",
            "gender",
            "country",
            "city",
            "address",
            "business_name",
            "business_address",
            "latitude",
            "longitude",
            "is_verified_provider",
            "description",
            "subscription_tier",
            "subscription_expires_at",
            "loyalty_points",
            "membership_duration",
        ]
        read_only_fields = ["pkid", "email", "date_joined"]

    def get_full_name(self, obj):
        return obj.get_fullname
