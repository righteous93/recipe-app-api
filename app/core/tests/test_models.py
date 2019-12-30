from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    # Here we are trying to check whether the intended user is created
    # with email and the password provided.
    # It may seem fruitless but its not so ... please analyze carefully
    def test_user_create_user_with_email_successful(self):
        """ Test creating a new user with an email is successful"""
        email = "savygaara@gmail.com"
        password = "Rogue@1993"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        # check_password() helper function comes with the django user Model
        # basically compares the user password with the password supplied.
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Test the email for the new user is normalized"""
        email = "savygaara@GMAIL.COM"
        user = get_user_model().objects.create_user(email, 'Rogue@1993')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test creating user without an email throws an error"""
        email = ""
        # just checking whether email does not violate the validation.
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(email, 'Rogue@1993')
            self.assertEqual(user.email, email.lower())
        # This method is called by the django commmand line to create a super
        # user. A user is said to be super user when the is_superuser is
        # is set as active or true

    def test_create_new_super_user(self):
        """ Test creating a new super user"""
        user = get_user_model().objects.create_superuser(
            "savygaara@gmail.com",
            "Rogue@1993"
        )
        # is_super is a part of the class
        # named PermissionsMixin
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
