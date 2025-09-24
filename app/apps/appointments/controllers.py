# apps/appointments/controllers.py
from datetime import datetime, timedelta, time, date
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from typing import List, Dict, Optional
import logging

from .models import ProviderAvailability, ProviderAvailabilityException, Appointment
from apps.services.models import Service
from apps.users.models import Profile

logger = logging.getLogger(__name__)


class AvailabilityController:
    """
    Controller for managing provider availability
    """

    @staticmethod
    def set_provider_availability(
        provider, day_of_week: int, start_time: time, end_time: time
    ):
        """Set or update provider's recurring availability for a specific day"""
        try:
            availability, created = ProviderAvailability.objects.update_or_create(
                provider=provider,
                day_of_week=day_of_week,
                defaults={
                    "start_time": start_time,
                    "end_time": end_time,
                    "is_available": True,
                },
            )
            return availability, created
        except Exception as e:
            logger.error(
                f"Error setting availability for provider {provider.id}: {str(e)}"
            )
            raise

    @staticmethod
    def get_provider_availability(provider):
        """Get all availability settings for a provider"""
        return ProviderAvailability.objects.filter(provider=provider, is_available=True)

    @staticmethod
    def delete_provider_availability(provider, availability_id):
        """Delete a specific availability setting"""
        try:
            availability = ProviderAvailability.objects.get(
                id=availability_id, provider=provider
            )
            availability.delete()
            return True
        except ProviderAvailability.DoesNotExist:
            return False

    @staticmethod
    def add_availability_exception(
        provider,
        exception_date: date,
        exception_type: str,
        start_time: time = None,
        end_time: time = None,
        reason: str = None,
    ):
        """Add availability exception (unavailable day, modified hours, etc.)"""
        try:
            exception = ProviderAvailabilityException.objects.create(
                provider=provider,
                exception_date=exception_date,
                exception_type=exception_type,
                start_time=start_time,
                end_time=end_time,
                reason=reason,
            )
            return exception
        except Exception as e:
            logger.error(
                f"Error creating availability exception for provider {provider.id}: {str(e)}"
            )
            raise

    @staticmethod
    def get_availability_exceptions(
        provider, start_date: date = None, end_date: date = None
    ):
        """Get availability exceptions for a provider within date range"""
        query = ProviderAvailabilityException.objects.filter(provider=provider)

        if start_date:
            query = query.filter(exception_date__gte=start_date)
        if end_date:
            query = query.filter(exception_date__lte=end_date)

        return query.order_by("exception_date")

    @staticmethod
    def get_provider_availability_for_date(provider, target_date: date) -> Dict:
        """
        Get provider's availability for a specific date considering:
        - Regular weekly availability
        - Date-specific exceptions
        """
        day_of_week = target_date.weekday()

        # Get regular availability for this day of week
        try:
            regular_availability = ProviderAvailability.objects.get(
                provider=provider, day_of_week=day_of_week, is_available=True
            )
        except ProviderAvailability.DoesNotExist:
            regular_availability = None

        # Check for exceptions
        try:
            exception = ProviderAvailabilityException.objects.get(
                provider=provider, exception_date=target_date
            )

            if exception.exception_type == "unavailable":
                return {"available": False, "reason": exception.reason}
            elif exception.exception_type == "modified_hours":
                return {
                    "available": True,
                    "start_time": exception.start_time,
                    "end_time": exception.end_time,
                    "modified": True,
                    "reason": exception.reason,
                }
            elif exception.exception_type == "available":
                # Override regular availability with specific hours
                return {
                    "available": True,
                    "start_time": exception.start_time,
                    "end_time": exception.end_time,
                    "modified": True,
                    "reason": exception.reason,
                }
        except ProviderAvailabilityException.DoesNotExist:
            pass

        # Return regular availability if no exceptions
        if regular_availability:
            return {
                "available": True,
                "start_time": regular_availability.start_time,
                "end_time": regular_availability.end_time,
                "modified": False,
            }

        return {"available": False, "reason": "No availability set for this day"}


class SlotController:
    """
    Controller for generating and managing available time slots
    """

    BASE_SLOT_DURATION = timedelta(minutes=30)  # Base slot duration for generation

    @staticmethod
    def generate_available_slots(
        provider, service, start_date: date, end_date: date, buffer_minutes: int = 0
    ) -> List[Dict]:
        """
        Generate available time slots for a provider and service within a date range
        """
        available_slots = []
        current_date = start_date

        while current_date <= end_date:
            # Get provider availability for this date
            availability = AvailabilityController.get_provider_availability_for_date(
                provider, current_date
            )

            if availability["available"]:
                slots_for_day = SlotController._generate_slots_for_date(
                    provider, service, current_date, availability, buffer_minutes
                )
                available_slots.extend(slots_for_day)

            current_date += timedelta(days=1)

        return available_slots

    @staticmethod
    def _generate_slots_for_date(
        provider, service, slot_date: date, availability: Dict, buffer_minutes: int
    ) -> List[Dict]:
        """Generate slots for a specific date based on availability"""
        slots = []

        # Calculate service duration
        service_duration = service.duration

        # Apply buffer time
        buffer_duration = timedelta(minutes=buffer_minutes)
        total_duration = service_duration + buffer_duration

        start_datetime = datetime.combine(slot_date, availability["start_time"])
        end_datetime = datetime.combine(slot_date, availability["end_time"])

        current_slot_start = start_datetime

        while current_slot_start + total_duration <= end_datetime:
            current_slot_end = current_slot_start + service_duration

            # Check if this slot is available (not booked and not in past)
            if current_slot_start > timezone.now() and SlotController.is_slot_available(
                provider, current_slot_start, current_slot_end
            ):

                slots.append(
                    {
                        "start_time": current_slot_start,
                        "end_time": current_slot_end,
                        "date": slot_date,
                        "duration_minutes": service_duration.total_seconds() / 60,
                    }
                )

            current_slot_start += SlotController.BASE_SLOT_DURATION

        return slots

    @staticmethod
    def is_slot_available(
        provider,
        start_time: datetime,
        end_time: datetime,
        exclude_appointment_id: str = None,
    ) -> bool:
        """
        Check if a time slot is available (not conflicting with existing appointments)
        exclude_appointment_id: Used when checking availability for an existing appointment (for rescheduling)
        """
        query = Appointment.objects.filter(
            provider=provider,
            scheduled_for__lt=end_time,
            scheduled_until__gt=start_time,
            status__in=["pending", "confirmed"],  # Only consider active appointments
        )

        if exclude_appointment_id:
            query = query.exclude(id=exclude_appointment_id)

        return not query.exists()


class AppointmentController:
    """
    Controller for managing appointments
    """

    @staticmethod
    @transaction.atomic
    def create_appointment(
        client,
        service,
        scheduled_for: datetime,
        scheduled_until: datetime,
        amount: float,
        currency: str = "XAF",
    ):
        """
        Create a new appointment with payment pending status
        """
        # Validate the slot is available
        if not SlotController.is_slot_available(
            service.provider, scheduled_for, scheduled_until
        ):
            raise ValueError("Selected time slot is no longer available")

        # Create the appointment
        appointment = Appointment.objects.create(
            client=client,
            provider=service.provider,
            service=service,
            scheduled_for=scheduled_for,
            scheduled_until=scheduled_until,
            amount=amount,
            currency=currency,
            status="pending",  # Will be confirmed after payment
            payment_status="pending",
        )

        logger.info(f"Appointment {appointment.id} created for client {client.id}")
        return appointment

    @staticmethod
    def confirm_appointment(appointment_id):
        """
        Confirm an appointment (after successful payment)
        """
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.status = "confirmed"
            appointment.confirmed_at = timezone.now()
            appointment.save()

            logger.info(f"Appointment {appointment.id} confirmed")
            return appointment
        except Appointment.DoesNotExist:
            raise ValueError("Appointment not found")

    @staticmethod
    def cancel_appointment(appointment_id, cancelled_by: str, reason: str = None):
        """
        Cancel an appointment
        """
        try:
            appointment = Appointment.objects.get(id=appointment_id)

            if cancelled_by == "client":
                appointment.status = "client_cancelled"
            elif cancelled_by == "provider":
                appointment.status = "provider_cancelled"
            else:
                raise ValueError("Invalid cancelled_by value")

            appointment.cancelled_at = timezone.now()
            appointment.save()

            logger.info(f"Appointment {appointment.id} cancelled by {cancelled_by}")
            return appointment
        except Appointment.DoesNotExist:
            raise ValueError("Appointment not found")

    @staticmethod
    def complete_appointment(appointment_id):
        """
        Mark an appointment as completed
        """
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.status = "completed"
            appointment.completed_at = timezone.now()
            appointment.save()

            logger.info(f"Appointment {appointment.id} marked as completed")
            return appointment
        except Appointment.DoesNotExist:
            raise ValueError("Appointment not found")

    @staticmethod
    def get_client_appointments(client, status_filter: str = None):
        """
        Get all appointments for a client
        """
        query = (
            Appointment.objects.filter(client=client)
            .select_related("provider", "provider__user", "service")
            .order_by("-scheduled_for")
        )

        if status_filter:
            query = query.filter(status=status_filter)

        return query

    @staticmethod
    def get_provider_appointments(provider, status_filter: str = None):
        """
        Get all appointments for a provider
        """
        query = (
            Appointment.objects.filter(provider=provider)
            .select_related("client", "client__user", "service")
            .order_by("-scheduled_for")
        )

        if status_filter:
            query = query.filter(status=status_filter)

        return query

    @staticmethod
    def reschedule_appointment(
        appointment_id, new_scheduled_for: datetime, new_scheduled_until: datetime
    ):
        """
        Reschedule an appointment to a new time
        """
        try:
            appointment = Appointment.objects.get(id=appointment_id)

            # Check if new slot is available (excluding this appointment)
            if not SlotController.is_slot_available(
                appointment.provider,
                new_scheduled_for,
                new_scheduled_until,
                appointment.id,
            ):
                raise ValueError("The selected time slot is no longer available")

            appointment.scheduled_for = new_scheduled_for
            appointment.scheduled_until = new_scheduled_until
            appointment.save()

            logger.info(
                f"Appointment {appointment.id} rescheduled to {new_scheduled_for}"
            )
            return appointment
        except Appointment.DoesNotExist:
            raise ValueError("Appointment not found")


class CalendarController:
    """
    Controller for calendar visualization and availability indicators
    """

    @staticmethod
    def get_monthly_availability_overview(
        provider, year: int, month: int
    ) -> Dict[date, str]:
        """
        Get daily availability status for a month (for calendar display)
        Returns: {date: 'full', 'limited', 'moderate', 'wide_open'}
        """
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)

        monthly_overview = {}
        current_date = start_date

        while current_date <= end_date:
            # Get basic availability
            availability = AvailabilityController.get_provider_availability_for_date(
                provider, current_date
            )

            if not availability["available"]:
                monthly_overview[current_date] = "full"  # Red - completely unavailable
            else:
                # Calculate actual occupancy for this day
                occupancy_data = CalendarController.get_day_availability_details(
                    provider, current_date
                )
                monthly_overview[current_date] = occupancy_data["availability_level"]

            current_date += timedelta(days=1)

        return monthly_overview

    @staticmethod
    def get_day_availability_details(provider, target_date: date) -> Dict:
        """
        Get detailed availability information for a specific day
        Includes booked slots, available slots, and occupancy percentage
        """
        # Get all appointments for the day
        day_start = datetime.combine(target_date, time.min)
        day_end = datetime.combine(target_date, time.max)

        appointments = Appointment.objects.filter(
            provider=provider,
            scheduled_for__date=target_date,
            status__in=["pending", "confirmed"],
        ).order_by("scheduled_for")

        # Calculate occupancy
        availability = AvailabilityController.get_provider_availability_for_date(
            provider, target_date
        )

        if not availability["available"]:
            return {
                "available": False,
                "occupancy_percentage": 100,
                "availability_level": "full",
                "booked_slots": [],
                "available_slots": [],
                "working_hours": None,
            }

        # Calculate total available minutes in the day
        start_time = availability["start_time"]
        end_time = availability["end_time"]
        total_minutes = (
            datetime.combine(target_date, end_time)
            - datetime.combine(target_date, start_time)
        ).total_seconds() / 60

        # Calculate booked minutes
        booked_minutes = 0
        booked_slots = []

        for appointment in appointments:
            appointment_duration = (
                appointment.scheduled_until - appointment.scheduled_for
            ).total_seconds() / 60
            booked_minutes += appointment_duration

            booked_slots.append(
                {
                    "start": appointment.scheduled_for,
                    "end": appointment.scheduled_until,
                    "client_name": appointment.client.user.get_fullname(),
                    "service_name": appointment.service.name,
                    "status": appointment.status,
                }
            )

        occupancy_percentage = (
            min(100, int((booked_minutes / total_minutes) * 100))
            if total_minutes > 0
            else 0
        )

        return {
            "available": True,
            "occupancy_percentage": occupancy_percentage,
            "availability_level": CalendarController._get_availability_level(
                occupancy_percentage
            ),
            "booked_appointments": booked_slots,
            "working_hours": {"start": start_time, "end": end_time},
            "total_booked_minutes": booked_minutes,
            "total_available_minutes": total_minutes,
        }

    @staticmethod
    def _get_availability_level(occupancy_percentage: int) -> str:
        """Convert occupancy percentage to availability level for UI colors"""
        if occupancy_percentage >= 90:
            return "full"  # Red
        elif occupancy_percentage >= 70:
            return "limited"  # Orange/Yellow
        elif occupancy_percentage >= 50:
            return "moderate"  # Light green
        else:
            return "wide_open"  # Green


class PaymentController:
    """
    Dummy payment controller - will be integrated with real payment providers later
    """

    @staticmethod
    def initiate_payment(
        appointment, payment_method: str, payment_details: dict
    ) -> dict:
        """Initiate payment for an appointment"""
        # This is a dummy implementation
        return {
            "success": True,
            "payment_id": f"pay_dummy_{appointment.uuid}",
            "status": "initiated",
            "message": "Payment initiated successfully",
            "next_step": "redirect_to_payment_gateway",
        }

    @staticmethod
    def confirm_payment(payment_id: str) -> dict:
        """Confirm payment was successful"""
        return {
            "success": True,
            "status": "held_in_escrow",
            "confirmed_at": timezone.now(),
        }

    @staticmethod
    def release_escrow_to_provider(appointment_id: str) -> dict:
        """Release escrow funds to provider"""
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.payment_status = "released_to_provider"
            appointment.save()

            return {
                "success": True,
                "status": "released_to_provider",
                "released_at": timezone.now(),
            }
        except Appointment.DoesNotExist:
            return {"success": False, "error": "Appointment not found"}

    @staticmethod
    def refund_escrow_to_client(appointment_id: str) -> dict:
        """Refund escrow funds to client"""
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.payment_status = "refunded_to_client"
            appointment.save()

            return {
                "success": True,
                "status": "refunded_to_client",
                "refunded_at": timezone.now(),
            }
        except Appointment.DoesNotExist:
            return {"success": False, "error": "Appointment not found"}
