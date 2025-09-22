# apps/appointments/serializers.py
from rest_framework import serializers
from .models import ProviderAvailability, ProviderAvailabilityException, Appointment
from apps.services.models import Service
from apps.users.models import Profile


class ProviderAvailabilitySerializer(serializers.ModelSerializer):
    day_of_week_display = serializers.CharField(
        source="get_day_of_week_display", read_only=True
    )

    class Meta:
        model = ProviderAvailability
        fields = [
            "id",
            "provider",
            "day_of_week",
            "day_of_week_display",
            "start_time",
            "end_time",
            "is_available",
        ]
        read_only_fields = ["id", "provider"]


class ProviderAvailabilityExceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderAvailabilityException
        fields = [
            "id",
            "provider",
            "exception_date",
            "exception_type",
            "start_time",
            "end_time",
            "reason",
        ]
        read_only_fields = ["id", "provider"]


class AppointmentCreateSerializer(serializers.ModelSerializer):
    service_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Appointment
        fields = [
            "service_id",
            "scheduled_for",
            "scheduled_until",
            "amount",
            "currency",
        ]

    def validate(self, data):
        # Check if service exists and is active
        try:
            service = Service.objects.get(id=data["service_id"], is_active=True)
        except Service.DoesNotExist:
            raise serializers.ValidationError("Service not found or inactive")

        data["service"] = service
        data["provider"] = service.provider

        # Validate scheduled times
        if data["scheduled_for"] >= data["scheduled_until"]:
            raise serializers.ValidationError("End time must be after start time")

        # Validate the slot is available
        from .controllers import SlotController

        if not SlotController.is_slot_available(
            data["provider"], data["scheduled_for"], data["scheduled_until"]
        ):
            raise serializers.ValidationError("This time slot is no longer available")

        return data


class AppointmentSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(
        source="client.user.get_fullname", read_only=True
    )
    provider_name = serializers.CharField(
        source="provider.user.get_fullname", read_only=True
    )
    service_name = serializers.CharField(source="service.name", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "uuid",
            "client",
            "client_name",
            "provider",
            "provider_name",
            "service",
            "service_name",
            "scheduled_for",
            "scheduled_until",
            "status",
            "payment_status",
            "amount",
            "currency",
            "confirmed_at",
            "cancelled_at",
            "completed_at",
            "created_at",
        ]
        read_only_fields = ["id", "uuid", "client", "provider", "created_at"]


class CalendarAvailabilitySerializer(serializers.Serializer):
    date = serializers.DateField()
    status = serializers.CharField()
    occupancy_percentage = serializers.IntegerField(required=False)
    availability_level = serializers.CharField(required=False)
