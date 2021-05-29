from apscheduler.schedulers.background import BackgroundScheduler
import atexit

class Schedule():
    scheduler = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls.scheduler is None:
            cls.scheduler = BackgroundScheduler(daemon=True)
            atexit.register(lambda: cls.scheduler.shutdown())
            cls.scheduler.start()
        return cls.scheduler