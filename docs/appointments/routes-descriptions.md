# Mubaku Appointments & Availability System Documentation

## Overview

The Mubaku Appointments System is designed to facilitate seamless booking experiences between clients and service providers. It handles provider availability management, real-time slot generation, appointment booking with escrow payments, and calendar visualization. The system ensures that clients can easily find and book available time slots while providers maintain control over their schedules.

---

## 1. Provider Availability Management

### 1.1 Manage Provider Availability
**Endpoint:** `GET/POST /availability/`

**Purpose:** This endpoint allows service providers to set up and manage their recurring weekly availability schedule. It's the foundation of the entire booking system - without availability settings, providers cannot accept appointments.

**How it works:**
- **GET**: Retrieves all existing availability settings for the authenticated provider, showing which days and times they're available for bookings throughout the week.
- **POST**: Creates or updates availability for a specific day of the week (Monday-Sunday). This sets the provider's standard working hours that repeat every week.

**Business Context:** Providers use this to establish their regular business hours. For example, a hair stylist might set Monday-Friday from 9 AM to 6 PM, ensuring clients can only book during these predefined times.

### 1.2 Delete Provider Availability
**Endpoint:** `DELETE /availability/{availability_id}/`

**Purpose:** Removes a specific availability setting when a provider no longer wants to offer services on a particular day of the week.

**How it works:** Permanently deletes the availability rule for that day. Future date calculations will no longer consider this day as available unless a new rule is created.

**Business Context:** Useful when a provider decides to stop working on certain days, like switching from 6-day to 5-day work weeks.

### 1.3 Manage Availability Exceptions
**Endpoint:** `GET/POST /availability/exceptions/`

**Purpose:** Handles one-time changes to a provider's regular schedule, such as holidays, special events, or unexpected closures.

**How it works:**
- **GET**: Retrieves all scheduled exceptions within an optional date range, helping providers review their special scheduling rules.
- **POST**: Creates new exceptions for specific dates, allowing providers to mark days as completely unavailable, available with modified hours, or specially available on normally off-days.

**Business Context:** Essential for real-world scheduling needs. For example, a provider can block Christmas Day, set shorter hours on New Year's Eve, or open specially on a Sunday for holiday season demand.

---

## 2. Slot and Appointment Management

### 2.1 Get Available Slots
**Endpoint:** `GET /services/{service_id}/slots/`

**Purpose:** The core discovery endpoint that shows clients exactly when a provider is available for a specific service.

**How it works:** Takes a service ID and date range, then calculates all available time slots by:
1. Checking the provider's regular availability for each day
2. Applying any date-specific exceptions
3. Considering existing appointments to avoid double-booking
4. Generating slots based on the service's duration
5. Applying buffer times between appointments

**Business Context:** This is what clients see when they're looking to book - a list of actual available times they can choose from. The system intelligently prevents overbooking and ensures realistic time allocations.

### 2.2 Create Appointment
**Endpoint:** `POST /appointments/`

**Purpose:** Allows clients to reserve a specific time slot with a provider for a service.

**How it works:** 
- Validates that the requested time slot is still available
- Creates an appointment in "pending" status
- Sets up the financial details but doesn't process payment immediately
- Prevents other clients from booking the same time slot

**Business Context:** This implements the "reserve now, pay later" flow. Clients can secure their preferred time without immediate payment pressure, reducing booking abandonment.

### 2.3 Confirm Appointment Payment
**Endpoint:** `POST /appointments/{appointment_id}/confirm-payment/`

**Purpose:** Finalizes the booking by processing payment and moving funds to escrow.

**How it works:** 
- Changes appointment status from "pending" to "confirmed"
- Updates payment status to "held_in_escrow"
- Marks the time slot as officially booked
- Triggers confirmation notifications

**Business Context:** This completes the booking transaction. Funds are held securely in escrow until service completion, protecting both clients and providers.

### 2.4 Cancel Appointment
**Endpoint:** `POST /appointments/{appointment_id}/cancel/`

**Purpose:** Handles appointment cancellations from either clients or providers with proper authorization.

**How it works:**
- Validates that the user has permission to cancel (client, provider, or admin)
- Updates appointment status to reflect who initiated the cancellation
- Frees up the time slot for other bookings
- Maintains audit trail of cancellation reason and timing

**Business Context:** Provides flexible cancellation policies while maintaining accountability and freeing up valuable appointment slots.

### 2.5 Reschedule Appointment
**Endpoint:** `POST /appointments/{appointment_id}/reschedule/`

**Purpose:** Allows clients to move their existing appointment to a different time slot.

**How it works:**
- Checks availability of the new requested time
- Updates the appointment with new timing if available
- Maintains all other appointment details and payment status
- Frees up the originally booked time slot

**Business Context:** Enhances customer experience by allowing flexibility when plans change, without requiring cancellation and rebooking.

### 2.6 Get My Appointments
**Endpoint:** `GET /appointments/my/`

**Purpose:** Provides users with a personalized view of all their appointments - both as a client and as a provider.

**How it works:**
- For clients: Shows all appointments they've booked
- For providers: Shows all appointments booked with them
- Optional filtering by status (pending, confirmed, completed, cancelled)
- Includes full details about the service, other party, and timing

**Business Context:** Serves as the primary dashboard for users to manage their bookings and schedule.

### 2.7 Get Appointment Detail
**Endpoint:** `GET /appointments/{appointment_id}/`

**Purpose:** Provides complete details for a specific appointment with proper access control.

**How it works:**
- Ensures only relevant parties (client, provider, admin) can view the appointment
- Returns comprehensive information including service details, timing, status, and payment information
- Serves as the single source of truth for any appointment-related inquiry

**Business Context:** Essential for customer support, dispute resolution, and providing users with complete transparency about their bookings.

---

## 3. Calendar Visualization

### 3.1 Monthly Calendar Overview
**Endpoint:** `GET /providers/{provider_id}/calendar/{year}/{month}/`

**Purpose:** Provides a high-level visual representation of a provider's availability for an entire month.

**How it works:**
- Calculates daily availability status for every day in the month
- Returns color-coded statuses: "full" (red), "limited" (orange), "moderate" (light green), "wide_open" (green)
- Considers both regular availability and exceptions
- Calculates occupancy based on existing bookings

**Business Context:** This powers the calendar UI that clients see when browsing providers. It gives instant visual feedback on which days have good availability without requiring detailed slot queries.

### 3.2 Day Availability Details
**Endpoint:** `GET /providers/{provider_id}/calendar/{year}/{month}/{day}/`

**Purpose:** Provides granular, minute-level detail about a specific day's schedule.

**How it works:**
- Shows exact working hours for the day
- Lists all booked appointments with client and service details
- Calculates occupancy percentage
- Provides availability level classification
- Shows total booked vs available minutes

**Business Context:** Useful for both clients wanting to see specific day details and providers managing their daily schedule. Helps understand why a day is classified as "limited" or "full" availability.

---

## System Architecture & Business Logic

### Availability Calculation Flow
1. **Base Schedule**: Regular weekly availability forms the foundation
2. **Exception Processing**: Date-specific overrides modify the base schedule
3. **Booking Consideration**: Existing appointments block specific time slots
4. **Slot Generation**: Available intervals are calculated based on service duration
5. **Buffer Application**: Time between appointments is reserved to prevent overlap

### Payment Integration Strategy
The system implements a two-phase payment process:
1. **Reservation Phase**: Time slot is temporarily held without payment
2. **Confirmation Phase**: Payment is processed and held in escrow

This approach reduces booking friction while maintaining financial security for both parties.

### Conflict Prevention
The system employs multiple layers of conflict prevention:
- Real-time availability checks during booking
- Atomic transactions to prevent race conditions
- Comprehensive validation of time slot boundaries
- Proper handling of time zones (currently Cameroon time)

### Scalability Considerations
- Date range limits prevent overwhelming calculations
- Efficient database indexing for quick availability queries
- Caching strategies for calendar views
- Background processing for complex calculations
