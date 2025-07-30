from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from mubaku.settings.constants import AppContants


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(_(AppContants.USER_EMAIL_VALIDATION_ERROR_MESSAGE))

    def create_user(
        self, username, first_name, last_name, email, password, **extra_fields
    ):
        """
        Create and save a user with the given email and password.
        """
        if not username:
            raise ValueError(_(AppContants.NO_USERNAME_ERROR_MESSAGE))
        if not first_name:
            raise ValueError(_(AppContants.NO_FIRSTNAME_ERROR_MESSAGE))
        if not last_name:
            raise ValueError(_(AppContants.NO_LASTNAME_ERROR_MESSAGE))
        if not password:
            raise ValueError(_(AppContants.NO_PASSWORD_ERROR_MESSAGE))
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)

        else:
            raise ValueError(_(AppContants.NO_EMAIL_SET_ERROR_MESSAGE))
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, first_name, last_name, email, password, **extra_fields
    ):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                _(AppContants.CREATE_SUPERUSER_IS_STAFF_IS_NOT_TRUE_ERROR_MESSAGE)
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                _(AppContants.CREATE_SUPERUSER_IS_SUPERUSER_IS_NOT_TRUE_ERROR_MESSAGE)
            )
        if not password:
            raise ValueError(_(AppContants.NO_PASSWORD_ERROR_MESSAGE))
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_(AppContants.NO_EMAIL_SET_ERROR_MESSAGE))

        return self.create_user(
            username, first_name, last_name, email, password, **extra_fields
        )
