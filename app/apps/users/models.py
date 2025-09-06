import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    Group,
    Permission,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from apps.core.models import Gender, TimeStampedUUIDModel
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("client", _("Client")),
        ("provider", _("Provider")),
        ("admin", _("Admin")),
        ("superuser", _("Superuser")),
    )
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pkid = models.BigAutoField(primary_key=True, editable=False)
    username = models.CharField(verbose_name=_("Username"), max_length=250)
    first_name = models.CharField(verbose_name=_("First Name"), max_length=250)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=250)
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), max_length=30, default="+237670181440"
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(default=timezone.now)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="client")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["phone_number"]),
            models.Index(fields=["role"]),
        ]

    def __str__(self) -> str:
        return self.username

    @property
    def get_fullname(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    def get_short_name(self):
        return self.username

    @property
    def membership_duration(self):
        """Returns time since account creation in human-readable format"""
        from django.utils.timesince import timesince

        return timesince(self.date_joined)

    @property
    def last_active(self):
        """Returns time since last login in human-readable format"""
        from django.utils.timesince import timesince

        return timesince(self.last_login) if self.last_login else "Never"


class Profile(TimeStampedUUIDModel):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    about_me = models.TextField(
        verbose_name=_("About me"),
        default="",
        blank=True,
        null=True,
    )
    profile_photo = models.ImageField(
        verbose_name=_("Profile Photo"), default="profiles/default_profile.png"
    )
    gender = models.CharField(
        verbose_name=_("Gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=20,
    )
    country = CountryField(
        verbose_name=_("Country"), default="CMR", blank=False, null=False
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=180,
        default="Bamenda",
        blank=False,
        null=False,
    )
    address = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        default="Address",
        verbose_name=_("Address"),
    )

    # Provider-specific fields
    business_name = models.CharField(max_length=255, blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=10, decimal_places=8, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=11, decimal_places=8, blank=True, null=True
    )
    is_verified_provider = models.BooleanField(
        verbose_name=_("Is Verified provider"),
        default=False,
        help_text=_("Indicates if the provider profile is verified by an admin."),
    )
    description = models.TextField(blank=True, null=True)
    subscription_tier = models.CharField(
        max_length=20,
        choices=(
            ("basic", _("Basic")),
            ("premium", _("Premium")),
            ("business", _("Business")),
        ),
        default="basic",
    )
    subscription_expires_at = models.DateTimeField(blank=True, null=True)

    # Client-specific fields
    loyalty_points = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=["latitude", "longitude"]),
            models.Index(fields=["is_verified_provider"]),
        ]

    def __str__(self) -> str:
        return f"{self.user.username}'s Profile"

    @property
    def joined_date(self):
        """Formatted account creation date"""
        return self.user.date_joined.strftime("%b %d, %Y")

    @property
    def last_login(self):
        """Formatted last login time"""
        return (
            self.user.last_login.strftime("%b %d, %Y %I:%M %p")
            if self.user.last_login
            else "Never"
        )
