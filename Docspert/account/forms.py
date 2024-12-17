from django.forms import ModelForm, ValidationError
from .models import Transaction, Account


class TransactionForm(ModelForm):
    def clean_account_id_from(self):
        account_id_from = self.cleaned_data.get("account_id_from")
        amount = self.data.get("amount")
        if account_id_from.balance < int(amount):
            raise ValidationError("Insufficient Funds in Account")

        return account_id_from

    class Meta:
        model = Transaction
        fields = ["note", "account_id_to", "account_id_from", "amount"]

