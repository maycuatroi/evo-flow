from evoflow.entities.core.base_object import BaseObject


class WorkFlow(BaseObject):
    def kill(self, **kwargs):
        pass

    def __info__(self, **kwargs) -> dict:
        current_job_index = self.jobs.index(self.current_job)
        info = {
            "jobs": len(self.jobs),
            "current job": f"{current_job_index} - {self.current_job.name}",
        }

    def __init__(self, name, jobs: list = [], **kwargs):
        super(WorkFlow, self).__init__(name=name, **kwargs)
        self.jobs = jobs
        self.current_job = self.jobs[0]

    def __dict__(self):
        data = {
            "jobs": [job.__dict__() for job in self.jobs],
            "current_job": self.current_job.name,
        }

        return data
