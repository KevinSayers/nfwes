from subprocess import Popen, PIPE
from pathlib import Path
from datetime import datetime


class Workflow(object):
    def __init__(self, run_id, request_data):
        self.run_id = run_id
        self.request_data = request_data
        self.run_obj = self.run()
        self.starttime = datetime.now()
        self.cmd = None



    def run(self):
        data = self.request_data
        # abs_wf_path = Path(data['workflow_url']).absolute()
        # print(abs_wf_path)
        wf_url = data['workflow_url']
        process = Popen(['nextflow', 'run', wf_url], stdout=PIPE, stderr=PIPE)
        return process

    def get_pid(self):
        return self.run_obj.pid

    def get_exit_code(self):
        return self.run_obj.returncode

    def check_running(self):
        return self.run_obj.poll()

    def get_state(self):
        state = None
        if self.check_running() is None:
            state = 'RUNNING'
        else:
            returncode = self.run_obj.returncode
            if returncode == 0:
                state = "COMPLETE"
            else:
                state = "EXECUTOR_ERROR"

        return state

    def get_status(self):
        out, err = self.run_obj.communicate()


        return {
            "run_id": self.run_id,
            "state": self.get_state(),
            "run_log": {
                "starttime": self.starttime,
                "stderr": err,
                "stdour": out
            }
        }


