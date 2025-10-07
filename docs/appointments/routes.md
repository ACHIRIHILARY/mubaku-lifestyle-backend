# Mubaku Appointments & Availability API Documentation

## Base URL
```
https://api.mubaku.com/api/appointments/
```

## Authentication
Most endpoints require JWT authentication. Include the token in the header:
```
Authorization: Bearer <your_jwt_token>
```

---

## 1. Provider Availability Management

### 1.1 Get/Set Provider Availability
**Endpoint:** `GET/POST /availability/`

**Permissions:** Provider only

#### GET - Get Provider Availability
**Response:**
```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "provider": "p1q2r3s4-t5u6-7890-abcd-ef1234567890",
    "day_of_week": 1,
    "day_of_week_display": "Monday",
    "start_time": "09:00:00",
    "end_time": "17:00:00",
    "is_available": true
  }
]
```

#### POST - Set Provider Availability
**Request Payload:**
```json
{
  "day_of_week": 1,
  "start_time": "09:00:00",
  "end_time": "17:00:00"
}
```

**Response:**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "provider": "p1q2r3s4-t5u6-7890-abcd-ef1234567890",
  "day_of_week": 1,
  "day_of_week_display": "Monday",
  "start_time": "09:00:00",
  "end_time": "17:00:00",
  "is_available": true
}
```

### 1.2 Delete Provider Availability
**Endpoint:** `DELETE /availability/{availability_id}/`

**Permissions:** Provider only

**Response:**
```json
{
  "message": "Availability setting deleted successfully"
}
```

### 1.3 Manage Availability Exceptions
**Endpoint:** `GET/POST /availability/exceptions/`

**Permissions:** Provider only

#### GET - Get Availability Exceptions
**Query Parameters:**
- `start_date` (optional): "2024-01-01"
- `end_date` (optional): "2024-01-31"

**Response:**
```json
[
  {
    "id": "b2c3d4e5-f6g7-8901-bcde-f23456789012",
    "provider": "p1q2r3s4-t5u6-7890-abcd-ef1234567890",
    "exception_date": "2024-12-25",
    "exception_type": "unavailable",
    "start_time": null,
    "end_time": null,
    "reason": "Christmas Holiday"
  }
]
```

#### POST - Create Availability Exception
**Request Payload:**
```json
{
  "exception_date": "2024-12-25",
  "exception_type": "unavailable",
  "reason": "Christmas Holiday"
}
```

**OR for modified hours:**
```json
{
  "exception_date": "2024-12-24",
  "exception_type": "modified_hours",
  "start_time": "10:00:00",
  "end_time": "14:00:00",
  "reason": "Christmas Eve - Short Day"
}
```

**Response:**
```json
{
  "id": "b2c3d4e5-f6g7-8901-bcde-f23456789012",
  "provider": "p1q2r3s4-t5u6-7890-abcd-ef1234567890",
  "exception_date": "2024-12-25",
  "exception_type": "unavailable",
  "start_time": null,
  "end_time": null,
  "reason": "Christmas Holiday"
}
```

---

## 2. Slot and Appointment Management

### 2.1 Get Available Slots
**Endpoint:** `GET /services/{service_id}/slots/`

**Permissions:** Public

**Query Parameters:**
- `start_date`: "2024-01-15" (required)
- `end_date`: "2024-01-20" (required)
- `buffer_minutes`: 15 (optional, default: 0)

**Response:**
```json
[
  {
    "start_time": "2024-01-15T09:00:00",
    "end_time": "2024-01-15T09:30:00",
    "date": "2024-01-15",
    "duration_minutes": 30
  },
  {
    "start_time": "2024-01-15T09:30:00",
    "end_time": "2024-01-15T10:00:00",
    "date": "2024-01-15",
    "duration_minutes": 30
  }
]
```

### 2.2 Create Appointment
**Endpoint:** `POST /appointments/`

**Permissions:** Client only

**Request Payload:**
```json
{
  "service_id": "s1e2r3v4-i5c6-7890-abcd-ef1234567890",
  "scheduled_for": "2024-01-15T09:00:00",
  "scheduled_until": "2024-01-15T09:30:00",
  "amount": 15000.00,
  "currency": "XAF"
}
```

**Response:**
```json
{
  "id": "a1p2p3o4-i5n6-7890-abcd-ef1234567890",
  "uuid": "b2c3d4e5-f6g7-8901-bcde-f23456789012",
  "client": "c1l2i3e4-n5t6-7890-abcd-ef1234567890",
  "client_name": "John Doe",
  "provider": "p1r2o3v4-i5d6-7890-abcd-ef1234567890",
  "provider_name": "Jane Smith",
  "service": "s1e2r3v4-i5c6-7890-abcd-ef1234567890",
  "service_name": "Hair Styling",
  "scheduled_for": "2024-01-15T09:00:00",
  "scheduled_until": "2024-01-15T09:30:00",
  "status": "pending",
  "payment_status": "pending",
  "amount": "15000.00",
  "currency": "XAF",
  "confirmed_at": null,
  "cancelled_at": null,
  "completed_at": null,
  "created_at": "2024-01-10T14:30:00"
}
```

### 2.3 Confirm Appointment Payment
**Endpoint:** `POST /appointments/{appointment_id}/confirm-payment/`

**Permissions:** Client (owner of appointment)

**Request Payload:** (None required - dummy implementation)

**Response:**
```json
{
  "id": "a1p2p3o4-i5n6-7890-abcd-ef1234567890",
  "uuid": "b2c3d4e5-f6g7-8901-bcde-f23456789012",
  "client": "c1l2i3e4-n5t6-7890-abcd-ef1234567890",
  "client_name": "John Doe",
  "provider": "p1r2o3v4-i5d6-7890-abcd-ef1234567890",
  "provider_name": "Jane Smith",
  "service": "s1e2r3v4-i5c6-7890-abcd-ef1234567890",
  "service_name": "Hair Styling",
  "scheduled_for": "2024-01-15T09:00:00",
  "scheduled_until": "2024-01-15T09:30:00",
  "status": "confirmed",
  "payment_status": "held_in_escrow",
  "amount": "15000.00",
  "currency": "XAF",
  "confirmed_at": "2024-01-10T15:00:00",
  "cancelled_at": null,
  "completed_at": null,
  "created_at": "2024-01-10T14:30:00"
}
```

### 2.4 Cancel Appointment
**Endpoint:** `POST /appointments/{appointment_id}/cancel/`

**Permissions:** Client, Provider, or Admin

**Request Payload:**
```json
{
  "reason": "Client emergency"
}
```

**Response:**
```json
{
  "id": "a1p2p3o4-i5n6-7890-abcd-ef1234567890",
  "uuid": "b2c3d4e5-f6g7-8901-bcde-f23456789012",
  "client": "c1l2i3e4-n5t6-7890-abcd-ef1234567890",
  "client_name": "John Doe",
  "provider": "p1r2o3v4-i5d6-7890-abcd-ef1234567890",
  "provider_name": "Jane Smith",
  "service": "s1e2r3v4-i5c6-7890-abcd-ef1234567890",
  "service_name": "Hair Styling",
  "scheduled_for": "2024-01-15T09:00:00",
  "scheduled_until": "2024-01-15T09:30:00",
  "status": "client_cancelled",
  "payment_status": "held_in_escrow",
  "amount": "15000.00",
  "currency": "XAF",
  "confirmed_at": "2024-01-10T15:00:00",
  "cancelled_at": "2024-01-11T10:00:00",
  "completed_at": null,
  "created_at": "2024-01-10T14:30:00"
}
```

### 2.5 Reschedule Appointment
**Endpoint:** `POST /appointments/{appointment_id}/reschedule/`

**Permissions:** Client (owner of appointment)

**Request Payload:**
```json
{
  "scheduled_for": "2024-01-16T10:00:00",
  "scheduled_until": "2024-01-16T10:30:00"
}
```

**Response:**
```json
{
  "id": "a1p2p3o4-i5n6-7890-abcd-ef1234567890",
  "uuid": "b2c3d4e5-f6g7-8901-bcde-f23456789012",
  "client": "c1l2i3e4-n5t6-7890-abcd-ef1234567890",
  "client_name": "John Doe",
  "provider": "p1r2o3v4-i5d6-7890-abcd-ef1234567890",
  "provider_name": "Jane Smith",
  "service": "s1e2r3v4-i5c6-7890-abcd-ef1234567890",
  "service_name": "Hair Styling",
  "scheduled_for": "2024-01-16T10:00:00",
  "scheduled_until": "2024-01-16T10:30:00",
  "status": "confirmed",
  "payment_status": "held_in_escrow",
  "amount": "15000.00",
  "currency": "XAF",
  "confirmed_at": "2024-01-10T15:00:00",
  "cancelled_at": null,
  "completed_at": null,
  "created_at": "2024-01-10T14:30:00"
}
```

### 2.6 Get My Appointments
**Endpoint:** `GET /appointments/my/`

**Permissions:** Authenticated users

**Query Parameters:**
- `status` (optional): "pending", "confirmed", "completed", "cancelled"

**Response:**
```json
[
  {
    "id": "a1p2p3o4-i5n6-7890-abcd-ef1234567890",
    "uuid": "b2c3d4e5-f6g7-8901-bcde-f23456789012",
    "client": "c1l2i3e4-n5t6-7890-abcd-ef1234567890",
    "client_name": "John Doe",
    "provider": "p1r2o3v4-i5d6-7890-abcd-ef1234567890",
    "provider_name": "Jane Smith",
    "service": "s1e2r3v4-i5c6-7890-abcd-ef1234567890",
    "service_name": "Hair Styling",
    "scheduled_for": "2024-01-15T09:00:00",
    "scheduled_until": "2024-01-15T09:30:00",
    "status": "confirmed",
    "payment_status": "held_in_escrow",
    "amount": "15000.00",
    "currency": "XAF",
    "confirmed_at": "2024-01-10T15:00:00",
    "cancelled_at": null,
    "completed_at": null,
    "created_at": "2024-01-10T14:30:00"
  }
]
```

### 2.7 Get Appointment Detail
**Endpoint:** `GET /appointments/{appointment_id}/`

**Permissions:** Client, Provider, or Admin (related to appointment)

**Response:**
```json
{
  "id": "a1p2p3o4-i5n6-7890-abcd-ef1234567890",
  "uuid": "b2c3d4e5-f6g7-8901-bcde-f23456789012",
  "client": "c1l2i3e4-n5t6-7890-abcd-ef1234567890",
  "client_name": "John Doe",
  "provider": "p1r2o3v4-i5d6-7890-abcd-ef1234567890",
  "provider_name": "Jane Smith",
  "service": "s1e2r3v4-i5c6-7890-abcd-ef1234567890",
  "service_name": "Hair Styling",
  "scheduled_for": "2024-01-15T09:00:00",
  "scheduled_until": "2024-01-15T09:30:00",
  "status": "confirmed",
  "payment_status": "held_in_escrow",
  "amount": "15000.00",
  "currency": "XAF",
  "confirmed_at": "2024-01-10T15:00:00",
  "cancelled_at": null,
  "completed_at": null,
  "created_at": "2024-01-10T14:30:00"
}
```

---

## 3. Calendar Views

### 3.1 Monthly Calendar Overview
**Endpoint:** `GET /providers/{provider_id}/calendar/{year}/{month}/`

**Permissions:** Public

**Response:**
```json
[
  {
    "date": "2024-01-01",
    "status": "full",
    "availability_level": "full"
  },
  {
    "date": "2024-01-02",
    "status": "limited",
    "availability_level": "limited"
  },
  {
    "date": "2024-01-03",
    "status": "wide_open",
    "availability_level": "wide_open"
  }
]
```

### 3.2 Day Availability Details
**Endpoint:** `GET /providers/{provider_id}/calendar/{year}/{month}/{day}/`

**Permissions:** Public

**Response:**
```json
{
  "available": true,
  "occupancy_percentage": 65,
  "availability_level": "moderate",
  "booked_appointments": [
    {
      "start": "2024-01-15T09:00:00",
      "end": "2024-01-15T09:30:00",
      "client_name": "John Doe",
      "service_name": "Haircut",
      "status": "confirmed"
    },
    {
      "start": "2024-01-15T11:00:00",
      "end": "2024-01-15T12:00:00",
      "client_name": "Sarah Johnson",
      "service_name": "Hair Coloring",
      "status": "confirmed"
    }
  ],
  "working_hours": {
    "start": "09:00:00",
    "end": "17:00:00"
  },
  "total_booked_minutes": 90,
  "total_available_minutes": 480
}
```

---

## Error Responses

### Common Error Formats

**400 Bad Request:**
```json
{
  "error": "Invalid date format. Use YYYY-MM-DD"
}
```

**403 Forbidden:**
```json
{
  "error": "Only providers can manage availability"
}
```

**404 Not Found:**
```json
{
  "error": "Appointment not found"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Failed to create appointment"
}
```

### Validation Errors:
```json
{
  "scheduled_for": ["This field is required."],
  "scheduled_until": ["End time must be after start time."]
}
```

---

## Status Codes Reference

### Appointment Status:
- `pending` - Created but payment not confirmed
- `confirmed` - Payment confirmed, appointment scheduled
- `declined` - Provider declined the appointment
- `client_cancelled` - Cancelled by client
- `provider_cancelled` - Cancelled by provider
- `completed` - Service completed

### Payment Status:
- `pending` - Payment not initiated
- `processing` - Payment in progress
- `held_in_escrow` - Payment held in escrow
- `released_to_provider` - Funds released to provider
- `refunded_to_client` - Funds refunded to client
- `failed` - Payment failed

### Availability Levels:
- `full` - Red (90-100% occupied)
- `limited` - Orange/Yellow (70-89% occupied)
- `moderate` - Light Green (50-69% occupied)
- `wide_open` - Green (0-49% occupied)

---

## Usage Flow Examples

### 1. Client Booking Flow:
1. **Get available slots**: `GET /services/{service_id}/slots/?start_date=2024-01-15&end_date=2024-01-20`
2. **Create appointment**: `POST /appointments/` (with selected slot)
3. **Confirm payment**: `POST /appointments/{appointment_id}/confirm-payment/`

### 2. Provider Setup Flow:
1. **Set availability**: `POST /availability/` (for each day of week)
2. **Add exceptions**: `POST /availability/exceptions/` (for holidays, etc.)
3. **View calendar**: `GET /providers/{provider_id}/calendar/2024/1/`

### 3. Management Flow:
1. **View appointments**: `GET /appointments/my/`
2. **Cancel if needed**: `POST /appointments/{appointment_id}/cancel/`
3. **Reschedule if needed**: `POST /appointments/{appointment_id}/reschedule/`

