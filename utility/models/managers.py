from django.db import models
from django.db.models import QuerySet

from utility.models import InheritanceManagerMixin


def filter_active_objects(queryset) -> QuerySet:
    return queryset.filter(is_deleted=False)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return filter_active_objects(super().get_queryset())


class ConcreteActiveManager(InheritanceManagerMixin, ActiveManager):
    def get_queryset(self):
        return super().get_queryset().select_subclasses()


class ConcreteManager(InheritanceManagerMixin, models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_subclasses()
