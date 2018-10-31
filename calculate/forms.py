
from django import forms
from propicker.models import UserAccount

class BookForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ('user_account_num', 'user_account_bank')