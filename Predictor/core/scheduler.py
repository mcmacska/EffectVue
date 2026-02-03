from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from data.manager import get_data
from training.manager import train_data

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.start()

def shutdown_scheduler():
    scheduler.shutdown()

# ---- jobs ----

async def data_collecting_and_training():
    # collect data and train model
    historic_price_data = get_data()
    train_data(historic_price_data)


async def daily_job():
    print("Running daily job")

def register_jobs():
    scheduler.add_job(
        data_collecting_and_training,
        CronTrigger.from_crontab("* * * * *"),  # every minute
        id="every_minute",
        replace_existing=True,
    )

    # scheduler.add_job(
    #     daily_job,
    #     CronTrigger.from_crontab("0 2 * * *"),  # 2am daily
    #     id="daily",
    #     replace_existing=True,
    # )
    print("Jobs registered")
