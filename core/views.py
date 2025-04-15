import json

import requests
from django.shortcuts import render
from .forms import ConversionForm
from django.conf import settings
from django.core.cache import cache

from .models import Currency

CURRENCY_SYMBOLS = {
    'UAH': '₴',
    'USD': '$',
    'EUR': '€',
    'GBP': '£'
}

FIAT_CODES = ['UAH', 'USD', 'EUR', 'GBP']


def get_price_from_coingecko(currency, fiat_symbol):
    crypto_id = currency.name.lower().replace(' ', '-')
    fiat = fiat_symbol.lower()
    cache_key = f"{crypto_id}_{fiat}"

    cached = cache.get(cache_key)
    if cached:
        print(f"[CACHE HIT] {cache_key} → {cached}")
        return cached

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={fiat}"
    print(f"[API CALL] {url}")
    response = requests.get(url)
    print(f"[API STATUS] {response.status_code}")
    print(f"[API RESPONSE] {response.text}")

    if response.status_code == 200:
        data = response.json()
        price = data.get(crypto_id, {}).get(fiat)
        if price:
            cache.set(cache_key, price, timeout=60)  # Кеш на 1 хв
            return price
    return None


def crypto_calculator(request):
    form = ConversionForm(request.POST or None)
    context = {'form': form}

    if request.method == 'POST' and form.is_valid():
        currency = form.cleaned_data['currency']
        crypto = currency.symbol.upper()
        fiat = form.cleaned_data['fiat_currency']
        amount = form.cleaned_data['amount']

        reverse = request.POST.get('reverse') == 'true'
        print(f"[REQUEST] crypto: {crypto}, fiat: {fiat}, amount: {amount}, reverse: {reverse}")

        price = get_price_from_coingecko(currency, fiat)

        if reverse:
            if price:
                result = amount / price
                formatted = f"{result:,.8f}".replace(",", " ").replace(".", ",")
                context['formatted'] = f"{formatted} {crypto}"
                print(f"[RESULT] {result} → {context.get('formatted', 'no format')}")
            else:
                context['error'] = f"🚫 Неможливо отримати курс {crypto} → {fiat}"
        else:
            if price:
                result = amount * price
                formatted = f"{result:,.2f}".replace(",", " ").replace(".", ",")
                context['formatted'] = f"{formatted} {CURRENCY_SYMBOLS[fiat]}"
                print(f"[RESULT] {result} → {context.get('formatted', 'no format')}")
            else:
                context['error'] = f"🚫 Неможливо отримати курс {crypto} → {fiat}"

        if settings.DEBUG:
            context['debug'] = f"Crypto: {crypto}, Fiat: {fiat}, Amount: {amount}, Reverse: {reverse}"

    return render(request, 'calculator/calculator.html', context)


def get_price_chart_data(currency, days, fiat):
    crypto_id = currency.name.lower().replace(" ", "-")
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency={fiat.lower()}&days={days}&interval=daily"
    response = requests.get(url)
    print(f"[DEBUG chart] {url}")
    print(f"[DEBUG chart] response: {response.status_code} → {response.text}")
    if response.status_code == 200:
        data = response.json()
        return [(entry[0], entry[1]) for entry in data.get("prices", [])]
    return []


def chart_view(request):
    selected_currency = None
    chart_data = []
    selected_days = '7'
    currencies = Currency.objects.all()

    if request.method == 'POST':
        selected_days = request.POST.get('days', '7')
        selected_currency = Currency.objects.filter(id=request.POST.get('currency')).first()
        if selected_currency:
            selected_fiat = request.POST.get('fiat', 'USD')
            chart_data = get_price_chart_data(selected_currency, selected_days, selected_fiat)
    fiat_currencies = ['USD', 'UAH', 'EUR', 'GBP']
    selected_fiat = request.POST.get('fiat', 'USD')
    periods = [1, 7, 30, 90, 180, 365]
    return render(request, 'calculator/chart.html', {
        'fiat_currencies': fiat_currencies,
        'selected_fiat': selected_fiat,
        'currencies': currencies,
        'selected_currency': selected_currency,
        'chart_data': json.dumps(chart_data),
        'selected_days': selected_days,
        'periods': periods  # ← додано
    })
