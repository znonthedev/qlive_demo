import string
import random
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token




# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, email, username, phone, password=None):
        if not email:
            raise ValueError("user must have an email address")
        if not username:
            raise ValueError("user must have username")

        # user = authenticate(username=username, password=password)

        user = self.model(
            email=self.normalize_email(email), username=username, password=password
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
            password=password,
        )
        # user.is_active = True

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.role = "admin"
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    user_admin = "admin"
    user_staff = "staff"

    user_choices = [
        (user_staff, "staff"),
        (user_admin, "admin"),
    ]

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    is_staff = models.BooleanField(default=True, null=True, blank=True)
    is_superuser = models.BooleanField(default=False, null=True, blank=True)
    # full_name = models.CharField(max_length=30, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True, default='') 
    phone = models.CharField(max_length=30, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    raw_password = models.CharField(max_length=128, null=True, blank=True)

    role = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        choices=user_choices,
        default=user_staff,
    )

    objects = AccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "phone",
        "email",
    ]

    def __str__(self) -> str:
        return self.username

    def __str__(self) -> str:
        return self.full_name

    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



def password_generater(length):
    length = 8
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    rnd = random.SystemRandom()
    return(''.join(rnd.choice(chars) for i in range(length)))


class PasswordRest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    otp = models.CharField(max_length=4, null=True, blank=True)
