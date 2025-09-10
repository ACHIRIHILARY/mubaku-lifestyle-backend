-- Mubaku Sample Data
-- This file populates the database with sample data for testing

-- Insert service categories
INSERT INTO service_categories (name, description, image_url) VALUES
('Haircuts', 'Professional haircuts for men, women, and children', '/images/haircuts.jpg'),
('Styling', 'Hair styling and treatment services', '/images/styling.jpg'),
('Beard Grooming', 'Beard trimming and shaping services', '/images/beard.jpg'),
('Nail Care', 'Manicure and pedicure services', '/images/nails.jpg'),
('Makeup', 'Professional makeup application', '/images/makeup.jpg');

-- Insert sample users (password is "password123" hashed with bcrypt)
INSERT INTO auth_user (email, phone_number, password_hash, first_name, last_name, role, is_active, is_staff, is_superuser) VALUES
-- Clients
('client1@example.com', '+237655000001', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'John', 'Doe', 'client', TRUE, FALSE, FALSE),
('client2@example.com', '+237655000002', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Jane', 'Smith', 'client', TRUE, FALSE, FALSE),
-- Providers
('provider1@example.com', '+237655000011', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Mike', 'Johnson', 'provider', TRUE, FALSE, FALSE),
('provider2@example.com', '+237655000012', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Sarah', 'Williams', 'provider', TRUE, FALSE, FALSE),
-- Admin
('admin@example.com', '+237655000100', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Admin', 'User', 'admin', TRUE, TRUE, TRUE);

-- Insert client profiles
INSERT INTO client_profile (user_id, avatar_url) VALUES
(1, '/avatars/client1.jpg'),
(2, '/avatars/client2.jpg');

-- Insert provider profiles
INSERT INTO provider_profile (user_id, business_name, business_address, latitude, longitude, description, is_verified, avatar_url, subscription_tier) VALUES
(3, 'Mike''s Barbershop', '123 Main Street, Douala', 4.051056, 9.767868, 'Professional barber with 10 years of experience', TRUE, '/avatars/provider1.jpg', 'premium'),
(4, 'Sarah''s Beauty Salon', '456 Elite Road, Yaounde', 3.848032, 11.502075, 'Specialized in hair styling and makeup', TRUE, '/avatars/provider2.jpg', 'business');

-- Insert admin profile
INSERT INTO admin_profile (user_id, permissions, department) VALUES
(5, '{"can_manage_users": true, "can_manage_content": true, "can_handle_disputes": true}', 'Operations');

-- Insert services
INSERT INTO services (provider_id, category_id, name, description, duration, price, currency) VALUES
-- Mike's services
(1, 1, 'Men''s Haircut', 'Professional men''s haircut with styling', '00:30:00', 5000.00, 'XAF'),
(1, 1, 'Children''s Haircut', 'Haircut for children under 12', '00:30:00', 4000.00, 'XAF'),
(1, 3, 'Beard Trim', 'Professional beard trimming and shaping', '00:20:00', 3000.00, 'XAF'),
-- Sarah's services
(2, 2, 'Women''s Hair Styling', 'Professional hair styling for women', '01:00:00', 10000.00, 'XAF'),
(2, 5, 'Bridal Makeup', 'Special bridal makeup package', '01:30:00', 25000.00, 'XAF'),
(2, 4, 'Manicure', 'Professional manicure service', '00:45:00', 8000.00, 'XAF');

-- Insert provider availability
INSERT INTO provider_availability (provider_id, day_of_week, start_time, end_time) VALUES
-- Mike's availability (Mon-Fri 9am-6pm, Sat 10am-4pm)
(1, 1, '09:00:00', '18:00:00'),
(1, 2, '09:00:00', '18:00:00'),
(1, 3, '09:00:00', '18:00:00'),
(1, 4, '09:00:00', '18:00:00'),
(1, 5, '09:00:00', '18:00:00'),
(1, 6, '10:00:00', '16:00:00'),
-- Sarah's availability (Tue-Sat 10am-7pm)
(2, 2, '10:00:00', '19:00:00'),
(2, 3, '10:00:00', '19:00:00'),
(2, 4, '10:00:00', '19:00:00'),
(2, 5, '10:00:00', '19:00:00'),
(2, 6, '10:00:00', '19:00:00');

-- Insert appointments
INSERT INTO appointments (client_id, provider_id, service_id, scheduled_for, scheduled_until, status, amount, currency, payment_status) VALUES
(1, 1, 1, NOW() + INTERVAL '2 days', NOW() + INTERVAL '2 days' + INTERVAL '30 minutes', 'confirmed', 5000.00, 'XAF', 'held_in_escrow'),
(2, 2, 4, NOW() + INTERVAL '3 days', NOW() + INTERVAL '3 days' + INTERVAL '1 hour', 'confirmed', 10000.00, 'XAF', 'held_in_escrow'),
(1, 2, 5, NOW() + INTERVAL '5 days', NOW() + INTERVAL '5 days' + INTERVAL '1 hour 30 minutes', 'pending', 25000.00, 'XAF', 'pending');

-- Insert appointment slots
INSERT INTO appointment_slots (provider_id, slot_start, slot_end, status, appointment_id) VALUES
(1, NOW() + INTERVAL '2 days', NOW() + INTERVAL '2 days' + INTERVAL '30 minutes', 'booked', 1),
(2, NOW() + INTERVAL '3 days', NOW() + INTERVAL '3 days' + INTERVAL '1 hour', 'booked', 2),
(2, NOW() + INTERVAL '5 days', NOW() + INTERVAL '5 days' + INTERVAL '1 hour 30 minutes', 'available', NULL);

-- Insert payments
INSERT INTO payments (appointment_id, from_user_id, to_user_id, amount, currency, payment_method, payment_method_details, external_transaction_id, status) VALUES
(1, 1, 3, 5000.00, 'XAF', 'mtn_momo', '{"phone": "+237655000001"}', 'MM123456789', 'held'),
(2, 2, 4, 10000.00, 'XAF', 'orange_money', '{"phone": "+237655000002"}', 'OM987654321', 'held');

-- Insert reviews
INSERT INTO reviews (appointment_id, client_id, provider_id, rating, comment) VALUES
(1, 1, 1, 5, 'Great haircut! Mike is very professional.');

-- Insert loyalty programs
INSERT INTO loyalty_programs (client_id, provider_id, points, visits) VALUES
(1, 1, 50, 1),
(2, 2, 100, 2);

-- Insert notifications
INSERT INTO notifications (user_id, title, message, notification_type, is_read) VALUES
(1, 'Appointment Confirmed', 'Your appointment with Mike''s Barbershop is confirmed for tomorrow at 10:00 AM', 'booking_confirmation', FALSE),
(2, 'Payment Received', 'Your payment of 10,000 XAF has been received and is held in escrow', 'payment_confirmation', TRUE);
