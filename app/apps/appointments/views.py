# apps/appointments/views.py
import logging
from datetime import datetime, date
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import ProviderAvailability, ProviderAvailabilityException, Appointment
from .serializers import (
    ProviderAvailabilitySerializer,
    ProviderAvailabilityExceptionSerializer,
    AppointmentCreateSerializer,
    AppointmentSerializer,
    CalendarAvailabilitySerializer,
)
from .controllers import (
    AvailabilityController,
    SlotController,
    AppointmentController,
    CalendarController,
    PaymentController,
)
from apps.services.models import Service
from apps.users.models import Profile

logger = logging.getLogger(__name__)


# Provider Availability Views
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def manage_provider_availability(request):
    """
    Get or set provider availability
    """
    if request.user.role != "provider":
        return Response(
            {"error": "Only providers can manage availability"},
            status=status.HTTP_403_FORBIDDEN,
        )

    provider = request.user.profile

    if request.method == "GET":
        availability = AvailabilityController.get_provider_availability(provider)
        serializer = ProviderAvailabilitySerializer(availability, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = ProviderAvailabilitySerializer(data=request.data)
        if serializer.is_valid():
            try:
                availability, created = (
                    AvailabilityController.set_provider_availability(
                        provider=provider,
                        day_of_week=serializer.validated_data["day_of_week"],
                        start_time=serializer.validated_data["start_time"],
                        end_time=serializer.validated_data["end_time"],
                    )
                )
                response_serializer = ProviderAvailabilitySerializer(availability)
                return Response(
                    response_serializer.data,
                    status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
                )
            except Exception as e:
                logger.error(f"Error setting availability: {str(e)}")
                return Response(
                    {"error": "Failed to set availability"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_provider_availability(request, availability_id):
    """
    Delete a specific availability setting
    """
    if request.user.role != "provider":
        return Response(
            {"error": "Only providers can manage availability"},
            status=status.HTTP_403_FORBIDDEN,
        )

    provider = request.user.profile
    success = AvailabilityController.delete_provider_availability(
        provider, availability_id
    )

    if success:
        return Response(
            {"message": "Availability setting deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
    else:
        return Response(
            {"error": "Availability setting not found"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def manage_availability_exceptions(request):
    """
    Get or create availability exceptions
    """
    if request.user.role != "provider":
        return Response(
            {"error": "Only providers can manage availability exceptions"},
            status=status.HTTP_403_FORBIDDEN,
        )

    provider = request.user.profile

    if request.method == "GET":
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        start_date_obj = (
            datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None
        )
        end_date_obj = (
            datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
        )

        exceptions = AvailabilityController.get_availability_exceptions(
            provider, start_date_obj, end_date_obj
        )
        serializer = ProviderAvailabilityExceptionSerializer(exceptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = ProviderAvailabilityExceptionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                exception = AvailabilityController.add_availability_exception(
                    provider=provider,
                    exception_date=serializer.validated_data["exception_date"],
                    exception_type=serializer.validated_data["exception_type"],
                    start_time=serializer.validated_data.get("start_time"),
                    end_time=serializer.validated_data.get("end_time"),
                    reason=serializer.validated_data.get("reason"),
                )
                response_serializer = ProviderAvailabilityExceptionSerializer(exception)
                return Response(
                    response_serializer.data, status=status.HTTP_201_CREATED
                )
            except Exception as e:
                logger.error(f"Error creating availability exception: {str(e)}")
                return Response(
                    {"error": "Failed to create availability exception"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Slot and Appointment Views
@api_view(["GET"])
@permission_classes([AllowAny])
def get_available_slots(request, service_id):
    """
    Get available time slots for a service
    """
    service = get_object_or_404(Service, id=service_id, is_active=True)

    # Get date range from query parameters
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    buffer_minutes = int(request.GET.get("buffer_minutes", 0))

    if not start_date_str or not end_date_str:
        return Response(
            {"error": "start_date and end_date parameters are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        return Response(
            {"error": "Invalid date format. Use YYYY-MM-DD"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Validate date range
    if start_date > end_date:
        return Response(
            {"error": "start_date must be before or equal to end_date"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if (end_date - start_date).days > 30:  # Limit to 30 days
        return Response(
            {"error": "Date range cannot exceed 30 days"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        available_slots = SlotController.generate_available_slots(
            provider=service.provider,
            service=service,
            start_date=start_date,
            end_date=end_date,
            buffer_minutes=buffer_minutes,
        )

        return Response(available_slots, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error generating available slots: {str(e)}")
        return Response(
            {"error": "Failed to generate available slots"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_appointment(request):
    """
    Create a new appointment (payment pending)
    """
    if request.user.role != "client":
        return Response(
            {"error": "Only clients can create appointments"},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = AppointmentCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            appointment = AppointmentController.create_appointment(
                client=request.user.profile,
                service=serializer.validated_data["service"],
                scheduled_for=serializer.validated_data["scheduled_for"],
                scheduled_until=serializer.validated_data["scheduled_until"],
                amount=serializer.validated_data["amount"],
                currency=serializer.validated_data.get("currency", "XAF"),
            )

            response_serializer = AppointmentSerializer(appointment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating appointment: {str(e)}")
            return Response(
                {"error": "Failed to create appointment"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_appointment_payment(request, appointment_id):
    """
    Confirm appointment after successful payment
    """
    appointment = get_object_or_404(
        Appointment, id=appointment_id, client=request.user.profile
    )

    if appointment.status != "pending":
        return Response(
            {"error": "Appointment is not in pending state"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        # In real implementation, this would verify payment with gateway
        payment_result = PaymentController.confirm_payment(
            f"pay_dummy_{appointment.uuid}"
        )

        if payment_result["success"]:
            confirmed_appointment = AppointmentController.confirm_appointment(
                appointment_id
            )
            appointment.payment_status = "held_in_escrow"
            appointment.save()

            response_serializer = AppointmentSerializer(confirmed_appointment)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Payment confirmation failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except Exception as e:
        logger.error(f"Error confirming appointment payment: {str(e)}")
        return Response(
            {"error": "Failed to confirm appointment payment"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_appointment(request, appointment_id):
    """
    Cancel an appointment
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Check if user has permission to cancel
    if (
        request.user.profile != appointment.client
        and request.user.profile != appointment.provider
        and request.user.role not in ["admin", "superuser"]
    ):
        return Response(
            {"error": "You do not have permission to cancel this appointment"},
            status=status.HTTP_403_FORBIDDEN,
        )

    cancelled_by = (
        "client" if request.user.profile == appointment.client else "provider"
    )
    reason = request.data.get("reason")

    try:
        cancelled_appointment = AppointmentController.cancel_appointment(
            appointment_id, cancelled_by, reason
        )

        response_serializer = AppointmentSerializer(cancelled_appointment)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error cancelling appointment: {str(e)}")
        return Response(
            {"error": "Failed to cancel appointment"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reschedule_appointment(request, appointment_id):
    """
    Reschedule an appointment to a new time
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Check if user has permission to reschedule
    if request.user.profile != appointment.client:
        return Response(
            {"error": "Only the client can reschedule this appointment"},
            status=status.HTTP_403_FORBIDDEN,
        )

    new_scheduled_for = request.data.get("scheduled_for")
    new_scheduled_until = request.data.get("scheduled_until")

    if not new_scheduled_for or not new_scheduled_until:
        return Response(
            {"error": "scheduled_for and scheduled_until are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        new_scheduled_for = datetime.fromisoformat(
            new_scheduled_for.replace("Z", "+00:00")
        )
        new_scheduled_until = datetime.fromisoformat(
            new_scheduled_until.replace("Z", "+00:00")
        )
    except (ValueError, AttributeError):
        return Response(
            {"error": "Invalid datetime format. Use ISO format"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        rescheduled_appointment = AppointmentController.reschedule_appointment(
            appointment_id, new_scheduled_for, new_scheduled_until
        )

        response_serializer = AppointmentSerializer(rescheduled_appointment)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error rescheduling appointment: {str(e)}")
        return Response(
            {"error": "Failed to reschedule appointment"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Calendar Views
@api_view(["GET"])
@permission_classes([AllowAny])
def get_monthly_calendar(request, provider_id, year, month):
    """
    Get monthly availability overview for a provider's calendar
    """
    provider = get_object_or_404(Profile, id=provider_id)

    try:
        monthly_overview = CalendarController.get_monthly_availability_overview(
            provider, year, month
        )

        # Convert to list for serialization
        calendar_data = [
            {
                "date": date_obj,
                "status": status,
                "availability_level": status,  # For consistency with frontend
            }
            for date_obj, status in monthly_overview.items()
        ]

        serializer = CalendarAvailabilitySerializer(calendar_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error getting monthly calendar: {str(e)}")
        return Response(
            {"error": "Failed to get calendar data"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_day_availability_details(request, provider_id, year, month, day):
    """
    Get detailed availability information for a specific day
    """
    provider = get_object_or_404(Profile, id=provider_id)

    try:
        target_date = date(year, month, day)
        day_details = CalendarController.get_day_availability_details(
            provider, target_date
        )

        return Response(day_details, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({"error": "Invalid date"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error getting day availability details: {str(e)}")
        return Response(
            {"error": "Failed to get day availability details"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# User Appointment Management
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_appointments(request):
    """
    Get current user's appointments
    """
    user = request.user

    if user.role == "client":
        appointments = AppointmentController.get_client_appointments(user.profile)
    elif user.role == "provider":
        appointments = AppointmentController.get_provider_appointments(user.profile)
    else:
        return Response(
            {"error": "Invalid user role for this operation"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    status_filter = request.GET.get("status")
    if status_filter:
        appointments = appointments.filter(status=status_filter)

    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_appointment_detail(request, appointment_id):
    """
    Get detailed information for a specific appointment
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Check if user has permission to view this appointment
    if (
        request.user.profile != appointment.client
        and request.user.profile != appointment.provider
        and request.user.role not in ["admin", "superuser"]
    ):
        return Response(
            {"error": "You do not have permission to view this appointment"},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = AppointmentSerializer(appointment)
    return Response(serializer.data, status=status.HTTP_200_OK)
