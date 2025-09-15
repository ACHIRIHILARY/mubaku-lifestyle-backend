from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from djoser.serializers import UserCreateSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from apps.users.models import Profile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="profile.gender")
    phone_number = PhoneNumberField(source="profile.phone_number")
    profile_photo = serializers.ImageField(source="profile.profile_photo")
    country = CountryField(source="profile.country")  # Fixed typo from 'county'
    city = serializers.CharField(source="profile.city")
    full_name = serializers.SerializerMethodField()

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
        ]

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
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    country = CountryField(name_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    joined_date = serializers.CharField(
        source="user.profile.joined_date", read_only=True
    )
    last_login = serializers.CharField(source="user.profile.last_login", read_only=True)
    membership_duration = serializers.CharField(
        source="user.membership_duration", read_only=True
    )
    role = serializers.SerializerMethodField(read_only=True)
    is_verified_agent = serializers.SerializerMethodField(read_only=True)
    is_verified_landlord = serializers.SerializerMethodField(read_only=True)
    my_agency_is_verified = serializers.SerializerMethodField(read_only=True)

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
            "enquiries",
            "gender",
            "phone_number",
            "profile_photo",
            "joined_date",
            "last_login",
            "membership_duration",
            "role",
            "is_verified_agent",
            "is_verified_landlord",
            "my_agency_is_verified",
        ]

    def get_full_name(self, obj):
        return obj.user.get_fullname

    def get_role(self, obj):
        return obj.user.role if obj.user.role else "user"

    def get_is_verified_agent(self, obj):
        return obj.user.profile.is_verified_agent

    def get_is_verified_landlord(self, obj):
        return obj.user.profile.is_verified_landlord

    def get_my_agency_is_verified(self, obj):
        return (
            obj.user.profile.my_agency_is_verified
            if hasattr(obj.user.profile, "my_agency_is_verified")
            else False
        )


class UpdateProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "profile_photo",
            "about_me",
            "gender",
            "country",
            "city",
        ]


class UnifiedProfileSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(source="profile.phone_number")
    profile_photo = serializers.ImageField(
        source="profile.profile_photo", required=False
    )
    about_me = serializers.CharField(source="profile.about_me", required=False)
    gender = serializers.CharField(source="profile.gender")
    country = CountryField(source="profile.country")
    city = serializers.CharField(source="profile.city")
    address = serializers.CharField(source="profile.address")
    full_name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    is_verified_agent = serializers.SerializerMethodField()
    is_verified_landlord = serializers.SerializerMethodField()
    my_agency_is_verified = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "pkid",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "profile_photo",
            "about_me",
            "gender",
            "country",
            "city",
            "address",
            "is_verified_agent",
            "role",
            "full_name",
        ]
        read_only_fields = ["pkid", "email"]

    def get_full_name(self, obj):
        return obj.get_fullname

    def get_role(self, obj):
        return obj.role if obj.role else "user"

    def get_is_verified_agent(self, obj):
        return obj.profile.is_verified_provider
