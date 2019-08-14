from rest_framework import serializers

from main.models import FavThing, ThingCategory, LogAction, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        """Meta class for the User serializer."""

        model = User
        fields = ('email',)


class ThingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        """Meta class for the Thing serializer."""

        model = ThingCategory
        user = serializers.SlugRelatedField(
            queryset=User.objects.all(),
            slug_field='id'
        )
        id = serializers.CharField(required=False, allow_blank=True)
        fields = ('name', 'user', 'id')


class FavThingSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta class for the Fav thing serializer."""

        model = FavThing
        category = serializers.SlugRelatedField(
            queryset=ThingCategory.objects.all(),
            slug_field='id'
        )
        user = serializers.SlugRelatedField(
            queryset=User.objects.all(),
            slug_field='id'
        )
        id = serializers.CharField(required=False, allow_blank=True)
        fields = ('id', 'title', 'ranking', 'description', 'category', 'metadata',
                  'user', 'date_added', 'date_modified')


class FavThingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta class for the fav thing update serializer."""

        model = FavThing
        id = serializers.IntegerField(read_only=True)
        ranking = serializers.CharField(required=False, allow_blank=True)
        title = serializers.CharField(required=False, allow_blank=True)
        description = serializers.CharField(required=False, allow_blank=True)
        category = serializers.SlugRelatedField(
            queryset=ThingCategory.objects.all(),
            slug_field='id'
        )
        fields = ('id', 'title', 'ranking', 'description', 'metadata', 'category')


class LogActionSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta class for the log action serializer."""

        model = LogAction

        fields = ('id', 'action', 'extra_details', 'log_time', 'responsible')
