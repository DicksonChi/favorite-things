import json
import os

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from main.models import User, ThingCategory, FavThing, LogAction


class UserTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='user@email.com'
        )

    def test_user_does_not_exist(self):
        email = 'test@email.com'
        response = self.client.get(
            reverse('main:find_user', kwargs={'email': email})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_does_exist(self):
        response = self.client.get(
            reverse('main:find_user', kwargs={'email': self.user.email})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), self.user.id)

    def test_add_user(self):
        email = 'test@email.com'
        response = self.client.post(
            reverse('main:add_user'), data={'email': email}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CategoryTests(TestCase):
    fixtures = (os.path.join(settings.FIXTURE_DIR, 'default_category.json'),)

    def setUp(self):
        self.user = User.objects.create_user(
            email='user@email.com'
        )

    def test_get_category_list(self):
        response = self.client.get(
            reverse('main:get_category', kwargs={'user': self.user.id})
        )
        self.assertEqual(response.data.get("code"), "010")
        self.assertEqual(isinstance(response.data.get("categories"), list), True)

    def test_add_category(self):
        user = self.user.id
        response = self.client.post(
            reverse('main:create_category'), data={'user': user, 'name': "test category 2"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("code"), "010")

        log_action = LogAction.objects.all()
        category = ThingCategory.objects.last()
        self.assertEqual(len(log_action), 1)
        self.assertEqual(category.name, "test category 2")


class FavoriteTests(TestCase):
    fixtures = (os.path.join(settings.FIXTURE_DIR, 'default_category.json'),)

    def setUp(self):
        self.user = User.objects.create_user(
            email='user@email.com'
        )
        self.category = ThingCategory.objects.create(
            name="test category",
            user=self.user
        )

    def test_get_favorite_list(self):
        response = self.client.get(
            reverse('main:get_fav_thing', kwargs={'category': self.category.id, 'user': self.user.id})
        )
        self.assertEqual(response.data.get("code"), "010")
        self.assertEqual(isinstance(response.data.get("favThings"), list), True)
        self.assertEqual(len(response.data.get("favThings")), 0)

        FavThing.objects.create(
            ranking=1,
            title="Test Fav",
            description="Test description",
            category=self.category,
            user=self.user
        )
        self.user.refresh_from_db()

        # check again after adding a favorite thing for this user
        response = self.client.get(
            reverse('main:get_fav_thing', kwargs={'category': self.category.id, 'user': self.user.id})
        )
        self.assertEqual(response.data.get("code"), "010")
        self.assertEqual(isinstance(response.data.get("favThings"), list), True)
        self.assertEqual(len(response.data.get("favThings")), 1)

    def test_add_favorite(self):
        user = self.user.id
        log_action_count_prev = LogAction.objects.count()
        response = self.client.post(
            reverse('main:create_fav_thing'), data={'user': user,
                                                    'title': "test fav",
                                                    'ranking': 1,
                                                    'description': "to test this description is working well",
                                                    'category': self.category.id
                                                    }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("code"), "010")

        log_action = LogAction.objects.all()
        fav_thing = FavThing.objects.last()
        self.assertEqual(len(log_action), log_action_count_prev+1)
        self.assertEqual(fav_thing.description, "to test this description is working well")

    def test_update_favorite(self):
        user = str(self.user.id)
        category = str(self.category.id)
        log_action_count_prev = LogAction.objects.count()

        fav_thing = FavThing.objects.create(
            ranking=1,
            title="Test Fav",
            description="Test description",
            category=self.category,
            user=self.user
        )
        fav_thing_des_prev = fav_thing.description

        self.assertNotEqual(fav_thing_des_prev, "to test this update description is working well")
        data = json.dumps({'user': user,
                           'title': "test fav",
                           'ranking': 1,
                           'description': "to test this update description is working well",
                           'category': category,
                           "metadata": "[]"
                           })
        response = self.client.put(
            reverse('main:update_thing', kwargs={'id': fav_thing.id}),
            data=data, content_type="application/json"
        )

        self.user.refresh_from_db()

        log_action = LogAction.objects.all()
        fav_thing = FavThing.objects.last()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(log_action), log_action_count_prev + 1)
        self.assertEqual(fav_thing.description, "to test this update description is working well")

    def test_delete_favorite_list(self):
        log_count_prev = LogAction.objects.count()
        fav = FavThing.objects.create(
            ranking=1,
            title="Test Fav",
            description="Test description",
            category=self.category,
            user=self.user
        )

        self.user.refresh_from_db()
        last_obj = FavThing.objects.last()
        self.assertEqual(fav.id, last_obj.id)

        response = self.client.delete(
            reverse('main:destroy_thing', kwargs={'id': fav.id})
        )

        log_count_now = LogAction.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(log_count_now, log_count_prev + 1)
