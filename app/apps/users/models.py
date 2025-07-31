import uuid

from apps.core.models import Gender, TimeStampedUUIDModel
from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    Group,
    Permission,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("client", "Client"),
        ("provider", "Provider"),
        ("admin", "Admin"),
        ("superuser", "Superuser"),
    )
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pkid = models.BigAutoField(primary_key=True, editable=False)
    username = models.CharField(verbose_name=_("Username"), max_length=250)
    first_name = models.CharField(verbose_name=_("First Name"), max_length=250)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=250)
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(default=timezone.now)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="regular")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Change this to avoid clash
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Change this to avoid clash
        blank=True,
    )

    @property
    def membership_duration(self):
        """Returns time since account creation in human-readable format"""
        return timesince(self.date_joined)

    @property
    def last_active(self):
        """Returns time since last login in human-readable format"""
        return timesince(self.last_login)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        return self.username

    @property
    def get_fullname(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    def get_short_name(self):
        return self.username


class Profile(TimeStampedUUIDModel):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), max_length=30, default="+237670181440"
    )
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
    is_verified_provider = models.BooleanField(
        verbose_name=_("Is Verified provider"),
        default=False,
        help_text=_("Indicates if the provider profile is verified by an admin."),
    )
    is_verified_landlord = models.BooleanField(
        verbose_name=_("Is Verified Landlord"),
        default=False,
        help_text=_("Indicates if the landlord profile is verified by an admin."),
    )

    address = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        default="Address",
        verbose_name=_("Address"),
    )

    def __str__(self) -> str:
        return f"{self.user.username}'s Profile"

    def get_profile_enquiries(self):
        enquiries = self.enquiries.all()
        return enquiries

    def get_profile_listings(self):
        # Convert each QuerySet to a list
        landed_properties = list(self.lands.all())
        properties = list(self.properties.all())
        car_properties = list(self.cars.all())

        # Combine all the lists
        all_properties = landed_properties + properties + car_properties

        return all_properties

    @property
    def joined_date(self):
        """Formatted account creation date"""
        # reutrn just the date and not the time
        return self.user.date_joined.strftime("%b %d, %Y")
        # return self.user.date_joined.strftime("%b %d, %Y %I:%M")

    @property
    def last_login(self):
        """Formatted last login time"""
        return (
            self.user.last_login.strftime("%b %d, %Y %I:%M %p")
            if self.user.last_login
            else "Never"
        )
