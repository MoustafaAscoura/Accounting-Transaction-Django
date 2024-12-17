from django.core.exceptions import ValidationError
from django.db import models


class Account(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=50)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(default=0, decimal_places=3, max_digits=12)

    @classmethod
    def find_accounts_by_query(cls, query_str: str) -> list:
        query = models.Q(id__contains=query_str) | models.Q(name__contains=query_str)
        return cls.objects.filter(query)

    @classmethod
    def get_all_objects(cls):
        return list(cls.objects.all())

    def __str__(self):
        return self.name


class Transaction(models.Model):
    note = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField(null=False)
    account_id_to = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="incoming_transactions",
                                      null=False)
    account_id_from = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="outgoing_transactions",
                                        null=False)

    def __str__(self):
        return f"{self.account_id_from.name} To {self.account_id_to.name}"

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.clean()
            self.account_id_from.balance -= self.amount
            self.account_id_from.save()
            self.account_id_to.balance += self.amount
            self.account_id_to.save()

        super().save(*args, **kwargs)

    def clean(self):
        if self.account_id_to_id == self.account_id_from_id:
            raise ValidationError('Cannot Transfer Funds to Self')
