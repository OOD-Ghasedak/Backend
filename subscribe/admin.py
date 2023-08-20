from django.contrib import admin

from subscribe.models import PurchasedSubscription, Subscriber, SubscriptionStatus


@admin.register(PurchasedSubscription)
class PurchasedSubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    pass


@admin.register(SubscriptionStatus)
class SubscriptionStatusAdmin(admin.ModelAdmin):
    pass
