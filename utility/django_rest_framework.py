from django.db.models import QuerySet
from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class ObjectRelatedFilterset(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        lookup_url_kwarg = view.lookup_url_kwarg or view.lookup_field

        assert lookup_url_kwarg in view.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        if hasattr(view, 'object_related_queryset'):
            model: QuerySet = view.object_related_queryset
            view.object_related = get_object_or_404(model, id=view.kwargs[lookup_url_kwarg])

        filter_kwargs = {view.lookup_field: view.kwargs[lookup_url_kwarg]}
        return queryset.filter(**filter_kwargs)


class GhasedakPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page-size'
    page_size = 10
    max_page_size = 100
