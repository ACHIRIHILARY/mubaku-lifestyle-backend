
---

# 📖 API Documentation – Django + Djoser Auth

This documentation invludes the following:

* Authentication (JWT endpoints)
* User management (register, login, me, update password/email, reset flows)
* Profile management (view/update)
* Request & Response payloads for each
* Notes about headers, errors, and special fields

## Follow Swagger or Redoc

Run the following commands
```bash

make generate-api-schema

make generate-api-schema-json
```

Visit the following URLs
Swagger UI → http://localhost:8000/api/schema/swagger-ui/

Redoc → http://localhost:8000/api/schema/redoc/

✅ See all endpoints (/auth/jwt/create/, /auth/users/me/, /profiles/...)
✅ View request/response payloads (generated from your serializers)
✅ Test endpoints directly in the browser


## Expected Endpoints (optional)

## 🔑 Authentication

### 1. Obtain JWT Token

`POST /api/v1/auth/jwt/create/`

Request:

```json
{
  "email": "jane@example.com",
  "password": "yourpassword"
}
```

Response:

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJh...",
  "access": "eyJ0eXAiOiJKV1QiLCJh..."
}
```

👉 Use the `access` token in headers:

```
Authorization: Bearer <access_token>
```

---

### 2. Refresh Token

`POST /api/v1/auth/jwt/refresh/`

Request:

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJh..."
}
```

Response:

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJh..."
}
```

---

### 3. Verify Token

`POST /api/v1/auth/jwt/verify/`

Request:

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJh..."
}
```

Response:

```json
{}
```

---

## 👤 User Endpoints

### 4. Register User

`POST /api/v1/auth/users/`

Request:

```json
{
  "username": "jane_doe",
  "email": "jane@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "password": "securePassword123"
}
```

Response:

```json
{
  "pkid": 1,
  "username": "jane_doe",
  "email": "jane@example.com",
  "first_name": "Jane",
  "last_name": "Doe"
}
```

---

### 5. Get Current User

`GET /api/v1/auth/users/me/`

Headers:

```
Authorization: Bearer <access_token>
```

Response:

```json
{
  "pkid": 1,
  "username": "jane_doe",
  "email": "jane@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "full_name": "Jane Doe",
  "gender": "Female",
  "phone_number": "+237670181440",
  "profile_photo": "/media/profiles/default_profile.png",
  "country": "Cameroon",
  "city": "Bamenda",
  "role": "client",
  "admin": false
}
```

---

### 6. Get User by ID

`GET /api/v1/auth/users/<pkid>/`

Response same as above but for that user.

---

### 7. Update Password

`POST /api/v1/auth/users/set_password/`

Request:

```json
{
  "current_password": "oldPass123",
  "new_password": "newPass456"
}
```

Response:

```json
{}
```

---

### 8. Update Email

`POST /api/v1/auth/users/set_email/`

Request:

```json
{
  "current_password": "oldPass123",
  "new_email": "new@example.com"
}
```

Response:

```json
{}
```

---

### 9. Reset Password (Request)

`POST /api/v1/auth/users/reset_password/`

Request:

```json
{
  "email": "jane@example.com"
}
```

Response:

```json
{}
```

---

### 10. Reset Password (Confirm)

`POST /api/v1/auth/users/reset_password_confirm/`

Request:

```json
{
  "uid": "MQ",
  "token": "set-password-token",
  "new_password": "myNewPassword123"
}
```

Response:

```json
{}
```

---

### 11. Activate Account

`POST /api/v1/auth/users/activation/`

Request:

```json
{
  "uid": "MQ",
  "token": "activation-token"
}
```

Response:

```json
{}
```

---

## 📝 Profile Endpoints

### 12. Get Profile (by User ID)

`GET /api/v1/profiles/<pkid>/`

Response:

```json
{
  "id": "uuid-of-profile",
  "username": "jane_doe",
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane@example.com",
  "full_name": "Jane Doe",
  "country": "Cameroon",
  "address": "Address",
  "about_me": "Hello, I am Jane.",
  "city": "Bamenda",
  "gender": "Female",
  "phone_number": "+237670181440",
  "profile_photo": "/media/profiles/default_profile.png",
  "joined_date": "Sep 15, 2025",
  "last_login": "Sep 15, 2025 12:05 PM",
  "membership_duration": "2 days",
  "role": "client",
  "is_verified_agent": false,
  "is_verified_landlord": false,
  "my_agency_is_verified": false
}
```

---

### 13. Update Profile

`PATCH /api/v1/profiles/<pkid>/`

Request:

```json
{
  "phone_number": "+237699000111",
  "profile_photo": "binary_or_base64_image",
  "about_me": "Software engineer from Bamenda.",
  "gender": "Male",
  "country": "Cameroon",
  "city": "Yaoundé"
}
```

Response:

```json
{
  "phone_number": "+237699000111",
  "profile_photo": "/media/profiles/jane_new.png",
  "about_me": "Software engineer from Bamenda.",
  "gender": "Male",
  "country": "Cameroon",
  "city": "Yaoundé"
}
```

---

## ⚠️ Error Responses

* **400 Bad Request** → Missing or invalid fields
* **401 Unauthorized** → Missing or invalid token
* **403 Forbidden** → Not allowed for your role
* **404 Not Found** → Object doesn’t exist

