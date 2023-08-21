from django.db.models import QuerySet
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin as DRFCreateModelMixin, ListModelMixin as DRFListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet as DRFGenericViewSet


class ObjectRelatedFilterset(BaseFilterBackend):

    def get_lookup_url_kwarg(self, view):
        lookup_url_kwarg = view.related_lookup_url_kwarg or view.related_lookup_field

        assert lookup_url_kwarg in view.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (view.__class__.__name__, lookup_url_kwarg)
        )
        return lookup_url_kwarg

    def get_lookup_url(self, view):
        lookup_url_kwarg = self.get_lookup_url_kwarg(view)
        return view.kwargs[lookup_url_kwarg]

    def get_related_object(self, view):
        lookup_url = self.get_lookup_url(view)
        object_related_queryset: QuerySet = getattr(view, 'object_related_queryset', None)
        assert object_related_queryset, (
            'Expected view %s to have `.object_related_queryset` field.' %
            view.__class__.__name__,
        )
        object_related = get_object_or_404(object_related_queryset, id=lookup_url)
        return object_related

    def filter_queryset(self, request, queryset, view):
        lookup_url = self.get_lookup_url(view)
        self.get_related_object(view)
        filter_kwargs = {view.related_lookup_field: lookup_url}
        return queryset.filter(**filter_kwargs)


class GhasedakPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page-size'
    page_size = 10
    max_page_size = 100


class GenericViewSet(DRFGenericViewSet):
    related_object = None

    def is_read_only_action(self):
        return self.action in ['retrieve', 'list']

    def get_permission_classes(self):
        assert self.permission_classes is not None, (
                "'%s' should either include a `permission_classes` attribute, "
                "or override the `get_permission_classes()` method."
                % self.__class__.__name__
        )
        return self.permission_classes

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        return [permission() for permission in self.get_permission_classes()]

    def set_related_object(self):
        if ObjectRelatedFilterset in self.filter_backends:
            self.related_object = ObjectRelatedFilterset().get_related_object(self)
            self.check_object_permissions(self.request, self.related_object)


class CreateModelMixin(DRFCreateModelMixin):
    def create(self, request, *args, **kwargs):
        self.set_related_object()
        return super().create(request, *args, **kwargs)


class ListModelMixin(DRFListModelMixin):
    def list(self, request, *args, **kwargs):
        self.set_related_object()
        return super().list(request, *args, **kwargs)


class ValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'ورودی مورد قبول نیست!'

    def __init__(self, detail=None, status_code=None):
        self.detail = detail or self.default_detail
        self.status_code = status_code or self.status_code
