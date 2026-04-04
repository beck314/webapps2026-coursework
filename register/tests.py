from django.contrib.auth.models import User
from django.test import TestCase

from register.models import User_Info


# Create your tests here.

class UserProfileTest(TestCase):

    def test_user_model_has_profile(self):
        user = User(username='test', email='test@test.test', password='tests')
        user.save()
        self.assertTrue(
            hasattr(user, 'profile_name'),
        )

    def test_idk_whats_happening(self):
        user2 = User(username='test2', email='test@test.test', password='tests')
        user2.save()
        user_info = user2.profile_name
        user_info.first_name = 'test'
        user_info.save()

        self.assertEqual(user_info.first_name, 'test')
