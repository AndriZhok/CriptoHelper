from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import check_price_alerts  # імпортуємо функцію перевірки

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_price_alerts, 'interval', minutes=1)  # перевіряємо щохвилини
    scheduler.start()