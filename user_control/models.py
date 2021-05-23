from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Must have an email address')

        if not name:
            raise ValueError('Must have a name')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_advertiser = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Email & Password are required by default.

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class AdvertiserModel(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    address = models.TextField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.name


class CustomerModel(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.name


class FeedbackModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
