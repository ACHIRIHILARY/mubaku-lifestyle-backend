# apps/services/serializers.py
from rest_framework import serializers
from .models import ServiceCategory, Service
from apps.users.serializers import ProfileSerializer


class ServiceCategorySerializer(serializers.ModelSerializer):
    service_count = serializers.SerializerMethodField(read_only=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = ServiceCategory
        fields = [
            "id",
            "pkid",
            "name",
            "description",
            "image_url",
            "is_active",
            "service_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "service_count"]

    def get_service_count(self, obj):
        return obj.service_set.filter(is_active=True).count()


class ServiceCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ["id", "pkid", "name", "description", "image_url", "is_active"]


class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    provider_name = serializers.CharField(
        source="provider.user.get_fullname", read_only=True
    )
    provider_business = serializers.CharField(
        source="provider.business_name", read_only=True
    )
    is_verified_provider = serializers.BooleanField(
        source="provider.is_verified_provider", read_only=True
    )

    # Duration in minutes for easier frontend handling
    duration_minutes = serializers.SerializerMethodField()

    # Price display with currency
    price_display = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            "id",
            "pkid",
            "name",
            "description",
            "category",
            "category_name",
            "provider",
            "provider_name",
            "provider_business",
            "is_verified_provider",
            "duration",
            "duration_minutes",
            "price",
            "currency",
            "price_display",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "provider"]

    def get_duration_minutes(self, obj):
        """Convert duration to total minutes"""
        return int(obj.duration.total_seconds() // 60)

    def get_price_display(self, obj):
        """Format price with currency symbol"""
        currency_symbols = {"XAF": "FCFA", "USD": "$", "EUR": "€"}
        symbol = currency_symbols.get(obj.currency, obj.currency)
        return f"{symbol} {obj.price}"


class ServiceCreateSerializer(serializers.ModelSerializer):
    duration_minutes = serializers.IntegerField(
        write_only=True, min_value=15, max_value=480
    )

    class Meta:
        model = Service
        fields = [
            "id",
            "pkid",
            "name",
            "description",
            "category",
            "duration_minutes",
            "price",
            "currency",
            "is_active",
        ]

    def create(self, validated_data):
        # Convert minutes to duration
        duration_minutes = validated_data.pop("duration_minutes")
        validated_data["duration"] = f"00:{duration_minutes:02d}:00"

        # Set the provider from the request user's profile
        validated_data["provider"] = self.context["request"].user.profile

        return super().create(validated_data)


class ServiceUpdateSerializer(serializers.ModelSerializer):
    duration_minutes = serializers.IntegerField(
        write_only=True, min_value=15, max_value=480, required=False
    )

    class Meta:
        model = Service
        fields = [
            "name",
            "description",
            "category",
            "duration_minutes",
            "price",
            "currency",
            "is_active",
        ]

    def update(self, instance, validated_data):
        duration_minutes = validated_data.pop("duration_minutes", None)
        if duration_minutes is not None:
            validated_data["duration"] = f"00:{duration_minutes:02d}:00"

        return super().update(instance, validated_data)


class ServiceDetailSerializer(ServiceSerializer):
    provider_details = ProfileSerializer(source="provider", read_only=True)

    class Meta(ServiceSerializer.Meta):
        fields = ServiceSerializer.Meta.fields + ["provider_details"]


class ProviderServiceStatsSerializer(serializers.Serializer):
    total_services = serializers.IntegerField()
    active_services = serializers.IntegerField()
    inactive_services = serializers.IntegerField()
    total_categories = serializers.IntegerField()
    average_price = serializers.DecimalField(max_digits=10, decimal_places=2)
