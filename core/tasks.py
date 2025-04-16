from django.utils import timezone
from .models import PriceWatch, UserNotification
from .views import get_price_from_coingecko

def check_price_alerts():
    print("[Scheduler] Checking price alerts...")

    watches = PriceWatch.objects.all()
    for watch in watches:
        now = timezone.now()
        if watch.last_checked and (now - watch.last_checked).total_seconds() < watch.period_minutes * 60:
            continue

        price = get_price_from_coingecko(watch.currency, watch.fiat_currency)
        if price is None:
            continue

        if watch.last_price and abs(price - watch.last_price) / watch.last_price > 0.0001:
            msg = f"💸 Ціна {watch.currency.symbol} змінилася з {watch.last_price:.2f} до {price:.2f} {watch.fiat_currency}"
            UserNotification.objects.create(user=watch.user, message=msg)

        watch.last_checked = now
        watch.last_price = price
        watch.save()