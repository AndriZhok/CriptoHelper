from django import forms
from .models import Currency, PriceWatch

FIAT_CHOICES = [
    ('UAH', '₴ Гривня'),
    ('USD', '$ Долар'),
    ('EUR', '€ Євро'),
    ('GBP', '£ Фунт'),
]

class ConversionForm(forms.Form):
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(), label="Криптовалюта", widget=forms.Select(attrs={'class': 'form-control'}))
    fiat_currency = forms.ChoiceField(choices=FIAT_CHOICES, label="Фіатна валюта", widget=forms.Select(attrs={'class': 'form-control'}))
    amount = forms.FloatField(label="Сума", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введіть суму'}))


class PriceWatchForm(forms.ModelForm):
    class Meta:
        model = PriceWatch
        fields = ['currency', 'fiat_currency', 'period_minutes']
        widgets = {
            'period_minutes': forms.NumberInput(attrs={'min': 1}),
        }