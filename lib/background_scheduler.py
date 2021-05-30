from apscheduler.schedulers.background import BackgroundScheduler
import atexit

class SchedulerModule():

    scheduler = None
    jobs = []
    
    def __init__(self):
        self.scheduler = BackgroundScheduler(daemon=True)
        atexit.register(lambda: self.scheduler.shutdown())
        self.scheduler.start()

    def add_job(self, **kwargs):
        self.jobs.append(self.scheduler.add_job(**kwargs))
        print("Job added: Size " + str(len(self.jobs)))

    def remove_job(self, id_):
        for i, job in enumerate(self.jobs[:]):
            if job.id == id_:
                try:
                    job.remove()
                    del jobs[i]
                    print("Job removed: Size " + str(len(self.jobs)))
                except:
                    return False
                return True
        return False

    def jobWithIdExists(self, id_):
        for job in self.jobs:
            if job.id == id_:
                return True
        return False
class Schedule():
    scheduler = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls.scheduler is None:
            cls.scheduler = SchedulerModule()
        return cls.scheduler