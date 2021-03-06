import factory
from django.test import TestCase

from main.models import User


class UserFactory(factory.DjangoModelFactory):
    email = 'test@email.com'

    class Meta:
        model = User
        django_get_or_create = ('email',)


class UserModelsTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create(email='test@test.com')

    def test_unicode(self):
        self.assertEqual(str(self.user), 'test@test.com')

    def test_super_user(self):
        super_user = User.objects.create_superuser(email='email@test.com')
        self.assertEqual(super_user.is_superuser, True)

    def test_user(self):
        user = User.objects.create_user(email='email@test.com')
        self.assertEqual(user.is_superuser, False)
