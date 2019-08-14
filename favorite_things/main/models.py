import uuid

from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def generate_mock_email():
    """Generate unique fake email."""
    return '{}@email.com'.format(uuid.uuid4())


class MyUserManager(BaseUserManager):
    def _create_user(
        self, email, password, first_name, last_name, is_staff, is_superuser, **extra_fields
    ):
        """
        Create and save an User with the given email, password, name and phone number.

        :param email: string
        :param password: string
        :param first_name: string
        :param last_name: string
        :param is_staff: boolean
        :param is_superuser: boolean
        :param extra_fields:
        :return: User
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, first_name='', last_name='', password=None, **extra_fields):
        """
        Create and save an User with the given email, and empty password since we don't need authentication.

        :param email: string
        :param first_name: string
        :param last_name: string
        :param password: string
        :param extra_fields:
        :return: User
        """

        return self._create_user(
            email, password, first_name, last_name, is_staff=False, is_superuser=False, **extra_fields
        )

    def create_superuser(self, email, first_name='', last_name='', password=None, **extra_fields):
        """
        Create a super user.

        :param email: string
        :param first_name: string
        :param last_name: string
        :param password: string
        :param extra_fields:
        :return: User
        """
        return self._create_user(
            email, password, first_name, last_name, is_staff=True, is_superuser=True, **extra_fields
        )


class User(AbstractUser):
    """
    Model that represents an user.

    To be active, the user must register and confirm his email.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # NOQA (ignore all errors on this line)
    email = models.EmailField(max_length=255, default=generate_mock_email, unique=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    username = models.CharField(max_length=200, default=uuid.uuid4, unique=False)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    class Meta:
        """Extra model properties."""

        ordering = ['-date_joined']

    def __str__(self):
        """
        Unicode representation for an user model.

        :return: string
        """
        return self.email


class FavAbstractModel(models.Model):
    """Creating the abstract base class for models in this app."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Define the meta properties of the class."""

        abstract = True


class ThingCategory(FavAbstractModel):
    name = models.CharField(max_length=20)
    user = models.ForeignKey('main.User', on_delete=models.CASCADE, null=True, related_name="category_user")
    system_default = models.BooleanField(default=False)

    def __str__(self):
        """
        Unicode representation for a ThingCategory model.

        :return: string
        """
        return self.name


class FavThing(FavAbstractModel):
    """Creating the model for the favorite thing the likes with it's properties."""

    title = models.CharField(max_length=20)
    ranking = models.IntegerField()
    description = models.CharField(max_length=200, null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('main.ThingCategory', on_delete=models.CASCADE, related_name="thing_category")
    user = models.ForeignKey('main.User', on_delete=models.CASCADE, null=True, related_name="thing_user")
    metadata = models.TextField(blank=True)

    class Meta:
        """Extra model properties."""

        ordering = ['category', 'ranking']

    def __str__(self):
        """
        Unicode representation for a FavThing model.

        :return: string
        """
        return '{} - {}'.format(
            str(self.shortened_id), self.title
        )

    @property
    def shortened_id(self):
        """
        Get shortened version of id.

        :return: first 8 characters of the ID

        """
        return str(self.id)[-8:]


class LogAction(models.Model):
    AUDIT_LOG_ADD = 0
    AUDIT_LOG_MODIFY = 1
    AUDIT_LOG_ADD_CATEGORY = 2
    AUDIT_LOG_DELETE = 3

    LOG_ACTION = (
        (AUDIT_LOG_ADD, 'Add Favorite Thing'),
        (AUDIT_LOG_MODIFY, 'Modify Favorite Thing'),
        (AUDIT_LOG_ADD_CATEGORY, 'Add a new category'),
        (AUDIT_LOG_DELETE, 'Delete a thing from the list.'),
    )

    class Meta:
        """Extra model properties."""

        ordering = ['-log_time']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action = models.IntegerField(choices=LOG_ACTION)
    extra_details = models.CharField(max_length=128, blank=True)
    log_time = models.DateTimeField(auto_now=True)
    responsible = models.ForeignKey('main.User', on_delete=models.CASCADE, null=True, related_name="responsible")
