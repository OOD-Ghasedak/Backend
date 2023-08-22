import math
from typing import TYPE_CHECKING

from django.db import models
from rest_framework.permissions import BasePermission

from channel_management.models import ChannelManager
from utility.models.managers import filter_active_objects

if TYPE_CHECKING:
    from channels.models import Channel


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj: 'Channel'):
        return obj.owner.ghased_id == request.ghased.id


class ChannelOwner(ChannelManager):
    channel = models.OneToOneField(
        to='channels.Channel',
        related_name='owner',
        on_delete=models.PROTECT,
        verbose_name='کانال'
    )

    def pay_to_admins(self, transaction: 'Transaction'):
        from financial.models import Transaction, Wallet
        entry = transaction.entries.filter(wallet__ghased_id=self.ghased_id).first()
        admins_to_pay = filter_active_objects(self.channel.admins).filter(share__isnull=False)
        wallets = Wallet.objects.filter(ghased_id__in=admins_to_pay.values_list('ghased', flat=True))
        admins_to_pay = dict(admins_to_pay.values_list('ghased_id', 'share'))
        payees = []
        amounts = []
        for wallet in wallets:
            payees.append(wallet)
            amounts.append(math.ceil(admins_to_pay[wallet.ghased] * entry.amount))
        Transaction.multi_pay(self.ghased.wallet, payees, amounts)

    class Meta:
        verbose_name = 'مالک کانال'
        verbose_name_plural = 'مالکین کانال‌ها'
