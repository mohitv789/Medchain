from django import forms
class TransactionForm(forms.Form):
    recipient = forms.CharField(max_length=100)
    amount = forms.IntegerField()

