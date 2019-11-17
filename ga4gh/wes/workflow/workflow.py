from subprocess import Popen, PIPE

import os

class Workflow(object):
    def __init__(self, run_id, request_data):
        self.run_id = run_id
        self.request_data = request_data
        self.run_obj = self.run()


    def run(self):
        data = self.request_data
        process = Popen(['nextflow', 'run', data['workflow_url']], stdout=PIPE, stderr=PIPE)
        return process

    def get_pid(self):
        return self.run_obj.pid

    def get_exit_code(self):
        return self.run_obj.returncode

    def check_running(self):
        return self.run_obj.poll()

    def get_status(self):

        status = None
        if self.check_running() is None:
            status = 'RUNNING'
        else:
            returncode = self.run_obj.returncode
            if returncode == 0:
                status = "COMPLETE"
            else:
                status = "EXECUTOR_ERROR"

        return {"run_id": self.run_id,
                "status": status}

