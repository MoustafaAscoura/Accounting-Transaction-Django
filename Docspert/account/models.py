from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(default=0, decimal_places=3, max_digits=12)


class Transaction(models.Model):
    note = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(null=False, decimal_places=3, max_digits=8)
    account_id_to = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="incoming_transactions")
    account_id_from = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="outgoing_transactions")
