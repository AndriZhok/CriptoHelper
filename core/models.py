from django.db import models
from django.conf import settings


class Currency(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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


class PriceWatch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    fiat_currency = models.CharField(max_length=10)
    period_minutes = models.IntegerField(default=10)  # періодичність у хвилинах
    last_checked = models.DateTimeField(null=True, blank=True)
    last_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} → {self.currency.symbol} ({self.fiat_currency})"


class UserNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


