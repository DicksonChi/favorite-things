import json

from django.db.models import Q, F
from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import FavThing, ThingCategory, LogAction, User
from main.serializers import (FavThingSerializer,
                              ThingCategorySerializer,
                              LogActionSerializer,
                              UserSerializer,
                              FavThingUpdateSerializer)


def reorder_ranking(ranking, category, user, current_ranking=None, operation="ADD"):
    """
    Reorder ranking function is responsible for reordering the ranking when there is an update.

    It is used by the FavThingsCreateView and FavThingsRetrieveUpdateView class.
    :param ranking: the new rank
    :param category: the category that is to be updated
    :param user: the user that owns the thing
    :param current_ranking: the current ranking before the update
    :param operation: the operation to be performed. Always defaults to ADD
    :return: doesnt return any parameter
    """
    similar_rank = FavThing.objects.filter(ranking=ranking,
                                           user__id=user,
                                           category__id=category).exists()
    if not similar_rank and operation != "DESTROY":
        return

    # ok for adding operation you increment.
    # for Editing swap.
    if operation == "ADD":
        FavThing.objects.filter(ranking__gte=ranking,
                                user__id=user,
                                category__id=category).update(ranking=F("ranking") + 1)
    elif operation == "DESTROY":
        FavThing.objects.filter(ranking__gte=ranking,
                                user__id=user,
                                category__id=category).update(ranking=F("ranking") - 1)

    else:
        FavThing.objects.filter(ranking=ranking,
                                user__id=user,
                                category__id=category).update(ranking=current_ranking)
        return


class UserCreateView(APIView):

    def post(self, request):
        """Handle the posting of data."""

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            response = {"code": "010",
                        "id": user.id,
                        "email": serializer.validated_data["email"],
                        }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {"code": "020",
                    "errors": serializer.errors
                    }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "email"

    def get(self, request, *args, **kwargs):
        """Handle retrieving user."""
        res = super(UserRetrieveView, self).get(request, *args, **kwargs)
        data = res.data
        data["code"] = "010"
        data["id"] = self.get_object().id
        return Response(data)


class GetCategory(generics.ListAPIView):
    serializer_class = ThingCategorySerializer
    lookup_field = "user"

    def list(self, request, *args, **kwargs):
        """Handle the list of categories found in the system."""

        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)

        res = {"code": "010",
               "categories": serializer.data
               }

        return Response(res)

    def get_queryset(self):
        """View to return a list of all the category for the user URL."""
        user = self.kwargs['user']

        return ThingCategory.objects.filter(Q(user__id=user) | Q(system_default=True))


class CategoryCreateView(APIView):
    serializer_class = ThingCategorySerializer

    def post(self, request):
        """Post new category to the list of categories."""
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            category = serializer.save()
            LogAction.objects.create(
                extra_details=f"A new category {category.name} was added to the list of categories. ",
                action=LogAction.AUDIT_LOG_ADD_CATEGORY,
                responsible=category.user
            )
            response = {"code": "010",
                        "message": "success"
                        }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {"code": "020",
                    "errors": serializer.errors
                    }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class GetFavThings(generics.ListAPIView):
    serializer_class = FavThingSerializer
    lookup_field = "category"

    def list(self, request, *args, **kwargs):
        """List of favorite things."""
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        for data in serializer.data:
            try:
                data['metadata'] = json.loads(data['metadata'])
            except Exception:  # NOQA (ignore all errors on this line)
                data['metadata'] = []
        res = {"code": "010",
               "favThings": serializer.data}
        return Response(res)

    def get_queryset(self):
        """Return a list of all the favorite things for the user."""
        category = self.kwargs['category']
        user = self.kwargs['user']
        return FavThing.objects.filter(category__id=category, user__id=user)


class FavThingsCreateView(APIView):
    serializer_class = FavThingSerializer

    def post(self, request):
        """Post the new favorite things to the db."""
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            reorder_ranking(data["ranking"], data['category'], data['user'])
            fav_thing = serializer.save()
            LogAction.objects.create(
                extra_details=f"A new thing {fav_thing.title} was added to {fav_thing.category.name} category. ",
                action=LogAction.AUDIT_LOG_ADD,
                responsible=fav_thing.user
            )
            response = {"code": "010",
                        "message": "success"
                        }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {"code": "020",
                    "errors": serializer.errors
                    }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class FavThingRetrieveUpdateView(generics.UpdateAPIView):
    queryset = FavThing.objects.all()
    serializer_class = FavThingUpdateSerializer
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        """Update the particular record."""
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except Http404:
            response = {"code": "020",
                        "errors": "not found"
                        }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            reorder_ranking(request.data["ranking"],
                            request.data['category'],
                            request.data['user'],
                            current_ranking=instance.ranking,
                            operation="UPDATE")
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}  # NOQA (ignore all errors on this line)

            LogAction.objects.create(
                extra_details=f"{self.get_object().title} was modified. ",
                action=LogAction.AUDIT_LOG_MODIFY,
                responsible=self.get_object().user
            )

            response = {"code": "010",
                        "status": "Updated the record"
                        }

            return Response(response, status=status.HTTP_200_OK)

        response = {"code": "020",
                    "errors": serializer.errors
                    }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class FavThingDestroy(generics.DestroyAPIView):
    serializer_class = FavThingUpdateSerializer
    lookup_field = "id"

    def get_queryset(self):
        """Queryset of all the log for the user for all their action."""
        thing_id = self.kwargs['id']
        return FavThing.objects.filter(id=thing_id)

    def destroy(self, request, *args, **kwargs):
        """Delete the particular record from the database."""
        rank = self.get_object().ranking
        category = self.get_object().category
        user = self.get_object().user
        name = self.get_object().title

        response = super(FavThingDestroy, self).destroy(request, *args, **kwargs)

        LogAction.objects.create(
            extra_details=f"{name} was deleted from {category.name}. ",
            action=LogAction.AUDIT_LOG_DELETE,
            responsible=user
        )
        reorder_ranking(ranking=rank, category=category.id, user=user.id, operation="DESTROY")
        return response


class GetUserLog(generics.ListAPIView):
    serializer_class = LogActionSerializer

    def list(self, request, *args, **kwargs):
        """List the list of favorite things."""
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        res = {"code": "010",
               "logs": serializer.data}
        return Response(res)

    def get_queryset(self):
        """Queryset of all the log for the user for all their action."""
        user_id = self.kwargs['user_id']
        return LogAction.objects.filter(responsible__id=user_id)
