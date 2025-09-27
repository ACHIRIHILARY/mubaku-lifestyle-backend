# apps/appointments/urls.py
from django.urls import path
from . import views

app_name = "appointments"

urlpatterns = [
    # Provider Availability
    path(
        "availability/", views.manage_provider_availability, name="manage-availability"
    ),
    path(
        "availability/<uuid:availability_id>/",
        views.delete_provider_availability,
        name="delete-availability",
    ),
    path(
        "availability/exceptions/",
        views.manage_availability_exceptions,
        name="manage-availability-exceptions",
    ),
    # Slots and Appointments
    path(
        "services/<uuid:service_id>/slots/",
        views.get_available_slots,
        name="get-available-slots",
    ),
    path("appointments/", views.create_appointment, name="create-appointment"),
    path("appointments/my/", views.get_my_appointments, name="my-appointments"),
    path(
        "appointments/<uuid:appointment_id>/",
        views.get_appointment_detail,
        name="appointment-detail",
    ),
    path(
        "appointments/<uuid:appointment_id>/confirm-payment/",
        views.confirm_appointment_payment,
        name="confirm-appointment-payment",
    ),
    path(
        "appointments/<uuid:appointment_id>/cancel/",
        views.cancel_appointment,
        name="cancel-appointment",
    ),
    path(
        "appointments/<uuid:appointment_id>/reschedule/",
        views.reschedule_appointment,
        name="reschedule-appointment",
    ),
    # Calendar
    path(
        "providers/<uuid:provider_id>/calendar/<int:year>/<int:month>/",
        views.get_monthly_calendar,
        name="monthly-calendar",
    ),
    path(
        "providers/<uuid:provider_id>/calendar/<int:year>/<int:month>/<int:day>/",
        views.get_day_availability_details,
        name="day-availability-details",
    ),
]
