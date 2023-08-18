from django.db.models import QuerySet
from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination


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
        filter_kwargs = {view.related_lookup_field: view.kwargs[lookup_url]}
        return queryset.filter(**filter_kwargs)


class GhasedakPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page-size'
    page_size = 10
    max_page_size = 100
