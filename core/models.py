from django.db import models
from django.conf import settings


class Currency(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)


class ConversionRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    fiat_currency = models.CharField(max_length=10)
    rate = models.FloatField()
    timestamp = models.DateTimeField()


class Alert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    target_price = models.FloatField()
    fiat_currency = models.CharField(max_length=10)
    triggered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class ConversionHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL)
    fiat_currency = models.CharField(max_length=10)
    amount = models.FloatField()
    result = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
