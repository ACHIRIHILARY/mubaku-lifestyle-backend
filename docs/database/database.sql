-- Mubaku Database Schema
-- PostgreSQL implementation with escrow payment system

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (base table for all users)
CREATE TABLE auth_user (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT uuid_generate_v4(),
    email VARCHAR(254) UNIQUE NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('client', 'provider', 'admin')),
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMPTZ,
    date_joined TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for auth_user
CREATE INDEX idx_auth_user_role ON auth_user(role);
CREATE INDEX idx_auth_user_phone ON auth_user(phone_number);
CREATE INDEX idx_auth_user_email ON auth_user(email);
CREATE INDEX idx_auth_user_created ON auth_user(created_at);

-- Client profile table
CREATE TABLE client_profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id) ON DELETE CASCADE,
    avatar_url TEXT,
    loyalty_points INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Provider profile table
CREATE TABLE provider_profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id) ON DELETE CASCADE,
    business_name VARCHAR(255),
    business_address TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    description TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    avatar_url TEXT,
    subscription_tier VARCHAR(20) DEFAULT 'basic' CHECK (subscription_tier IN ('basic', 'premium', 'business')),
    subscription_expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for provider_profile
CREATE INDEX idx_provider_profile_location ON provider_profile(latitude, longitude);
CREATE INDEX idx_provider_profile_verified ON provider_profile(is_verified);
CREATE INDEX idx_provider_profile_subscription ON provider_profile(subscription_tier, subscription_expires_at);

-- Admin profile table
CREATE TABLE admin_profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id) ON DELETE CASCADE,
    permissions JSONB,
    department VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Service categories table
CREATE TABLE service_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    image_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Services table
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    provider_id INTEGER NOT NULL REFERENCES provider_profile(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES service_categories(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    duration INTERVAL NOT NULL DEFAULT '30 minutes',
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    currency VARCHAR(3) NOT NULL DEFAULT 'XAF',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for services
CREATE INDEX idx_services_provider ON services(provider_id);
CREATE INDEX idx_services_category ON services(category_id);
CREATE INDEX idx_services_active ON services(is_active);

-- Provider availability table
CREATE TABLE provider_availability (
    id SERIAL PRIMARY KEY,
    provider_id INTEGER NOT NULL REFERENCES provider_profile(id) ON DELETE CASCADE,
    day_of_week SMALLINT NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(provider_id, day_of_week)
);

-- Provider availability exceptions table
CREATE TABLE provider_availability_exceptions (
    id SERIAL PRIMARY KEY,
    provider_id INTEGER NOT NULL REFERENCES provider_profile(id) ON DELETE CASCADE,
    exception_date DATE NOT NULL,
    exception_type VARCHAR(20) NOT NULL CHECK (exception_type IN ('unavailable', 'available', 'modified_hours')),
    start_time TIME,
    end_time TIME,
    reason VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(provider_id, exception_date)
);

-- Indexes for provider_availability_exceptions
CREATE INDEX idx_availability_exceptions ON provider_availability_exceptions(provider_id, exception_date);

-- Appointment slots table (for double-booking prevention)
CREATE TABLE appointment_slots (
    id SERIAL PRIMARY KEY,
    provider_id INTEGER NOT NULL REFERENCES provider_profile(id) ON DELETE CASCADE,
    slot_start TIMESTAMPTZ NOT NULL,
    slot_end TIMESTAMPTZ NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'available' CHECK (status IN ('available', 'booked', 'blocked')),
    appointment_id INTEGER, -- Will be added later with foreign key after appointments table is created
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Appointments table
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT uuid_generate_v4(),
    client_id INTEGER NOT NULL REFERENCES client_profile(id) ON DELETE CASCADE,
    provider_id INTEGER NOT NULL REFERENCES provider_profile(id) ON DELETE CASCADE,
    service_id INTEGER NOT NULL REFERENCES services(id) ON DELETE CASCADE,
    scheduled_for TIMESTAMPTZ NOT NULL,
    scheduled_until TIMESTAMPTZ NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN (
        'pending', 'confirmed', 'declined', 'client_cancelled', 
        'provider_cancelled', 'completed'
    )),
    amount DECIMAL(10, 2) NOT NULL CHECK (amount >= 0),
    currency VARCHAR(3) NOT NULL,
    payment_status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (payment_status IN (
        'pending', 'processing', 'held_in_escrow', 'released_to_provider', 
        'refunded_to_client', 'failed'
    )),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    confirmed_at TIMESTAMPTZ,
    cancelled_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ
);

-- Add foreign key to appointment_slots after appointments is created
ALTER TABLE appointment_slots 
ADD CONSTRAINT fk_appointment_slots_appointment 
FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE SET NULL;

-- Indexes for appointments
CREATE INDEX idx_appointments_client ON appointments(client_id);
CREATE INDEX idx_appointments_provider ON appointments(provider_id);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_appointments_payment_status ON appointments(payment_status);
CREATE INDEX idx_appointments_datetime ON appointments(scheduled_for);

-- Indexes for appointment_slots
CREATE INDEX idx_appointment_slots_provider ON appointment_slots(provider_id);
CREATE INDEX idx_appointment_slots_datetime ON appointment_slots(slot_start, slot_end);
CREATE INDEX idx_appointment_slots_status ON appointment_slots(status);
CREATE UNIQUE INDEX idx_appointment_slots_unique ON appointment_slots(provider_id, slot_start);

-- Payments table (financial ledger)
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    appointment_id INTEGER NOT NULL REFERENCES appointments(id),
    from_user_id INTEGER NOT NULL REFERENCES auth_user(id),
    to_user_id INTEGER NOT NULL REFERENCES auth_user(id),
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    payment_method VARCHAR(50) NOT NULL CHECK (payment_method IN ('mtn_momo', 'orange_money', 'card')),
    payment_method_details JSONB,
    external_transaction_id VARCHAR(255),
    escrow_release_trigger VARCHAR(50),
    status VARCHAR(50) NOT NULL CHECK (status IN (
        'initiated', 'processing', 'success', 'failed', 'held', 'released', 'refunded'
    )),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    processed_at TIMESTAMPTZ,
    held_until TIMESTAMPTZ,
    released_at TIMESTAMPTZ
);

-- Indexes for payments
CREATE INDEX idx_payments_appointment ON payments(appointment_id);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_payments_external_id ON payments(external_transaction_id);

-- Reviews table
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    appointment_id INTEGER UNIQUE NOT NULL REFERENCES appointments(id),
    client_id INTEGER NOT NULL REFERENCES client_profile(id),
    provider_id INTEGER NOT NULL REFERENCES provider_profile(id),
    rating SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for reviews
CREATE INDEX idx_reviews_provider ON reviews(provider_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);

-- Disputes table
CREATE TABLE disputes (
    id SERIAL PRIMARY KEY,
    appointment_id INTEGER UNIQUE NOT NULL REFERENCES appointments(id),
    raised_by_user_id INTEGER NOT NULL REFERENCES auth_user(id),
    reason TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'in_review', 'resolved')),
    admin_notes TEXT,
    resolved_by_admin_id INTEGER REFERENCES auth_user(id),
    resolved_at TIMESTAMPTZ,
    resolution VARCHAR(20) CHECK (resolution IN ('payment_released', 'payment_refunded')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for disputes
CREATE INDEX idx_disputes_appointment ON disputes(appointment_id);
CREATE INDEX idx_disputes_status ON disputes(status);

-- Escrow release schedule table (for automatic escrow releases)
CREATE TABLE escrow_release_schedule (
    id SERIAL PRIMARY KEY,
    appointment_id INTEGER NOT NULL REFERENCES appointments(id),
    scheduled_release_time TIMESTAMPTZ NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'processed', 'cancelled')),
    processed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for escrow_release_schedule
CREATE INDEX idx_escrow_release_schedule ON escrow_release_schedule(scheduled_release_time, status);

-- Notification table
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(50) NOT NULL CHECK (notification_type IN (
        'appointment_reminder', 'payment_confirmation', 'booking_confirmation',
        'review_request', 'promotional'
    )),
    is_read BOOLEAN DEFAULT FALSE,
    related_entity_type VARCHAR(50),
    related_entity_id INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for notifications
CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(is_read);
CREATE INDEX idx_notifications_created ON notifications(created_at);

-- Loyalty program table
CREATE TABLE loyalty_programs (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES client_profile(id),
    provider_id INTEGER NOT NULL REFERENCES provider_profile(id),
    points INTEGER NOT NULL DEFAULT 0,
    visits INTEGER NOT NULL DEFAULT 0,
    last_visit TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(client_id, provider_id)
);

-- Indexes for loyalty_programs
CREATE INDEX idx_loyalty_client ON loyalty_programs(client_id);
CREATE INDEX idx_loyalty_provider ON loyalty_programs(provider_id);
