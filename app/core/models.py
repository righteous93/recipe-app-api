from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                       PermissionsMixin


class UserManager(BaseUserManager):
    # This  create_user actually is overridden and will be called when we used
    # get_user_model().objects.create_user() in testing package that we have
    # created
    def create_user(self, email, password=None, **extra_fields):
        """ Creates and saves a new user"""

        #  A way of creating a new user model thats how the commands work
        # Basically we are creating the existing user model class provided by
        # the Django itself.
        # Raising the exception of value error when no email id is passed
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), password=password,
                          **extra_fields)

        # The password cannot be saved plainly the below method saves it
        # it in encrypted manner.

        user.set_password(password)
        # The command below self.db is used for supporting multiple databases
        # also for saving the new db schema
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Creates and saves a new super user """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Inherting the Below mentioned classes helps us use the Django provided
# features
# Out of the box
# This has to be mentioned in the settings.py in the app folder , just
# to make
# it explicit that we are gonna use email as username in the user model
# that we have created
class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    # unique field mentioned above makes the each user to have unique email id
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # users are active defaulty
    is_staff = models.BooleanField(default=False)  # Are not staff by default

    # We are creating a user manager here.
    objects = UserManager()
    # By default the USERNAM_FIELD is username, as we are planning to use the
    # email as the user name, thus the below mentioned assignment
    USERNAME_FIELD = 'email'
