from subprocess import Popen, PIPE
from pathlib import Path
from datetime import datetime
import os

class Workflow(object):
    def __init__(self, run_id, request_data):
        self.run_id = run_id
        self.run_dir = self.setup_rundir()
        self.request_data = request_data
        self.starttime = datetime.now()
        self.run_attachments = self.get_attachments()
        self.cmd = None
        self.engine_params = self.get_engine_params()
        self.workflow_params = self.get_wf_params()
        self.run_obj = self.run()
        self.tags = self.get_run_tags()


    def run(self):
        data = self.request_data
        wf_url = self.runnable_url(data['workflow_url'])
        process = Popen(['nextflow',
                         'run',
                         wf_url,
                         self.workflow_params,
                         self.engine_params,
                         ],
                        cwd=self.run_dir,
                        stdout=PIPE,
                        stderr=PIPE)
        return process

    def runnable_url(self, url):
        if 'https://' in url:
            return url
        if 'file://' in url:
            os.symlink(url[7:], os.path.join(self.run_dir, "nfwes.nf"))
            return os.path.join(self.run_dir, "nfwes.nf")


    def setup_rundir(self):
        Path(f'/home/kevin/worknfwes/{self.run_id}').mkdir(parents=True, exist_ok=True)
        return (f'/home/kevin/worknfwes/{self.run_id}')

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
            "tags": self.tags,
            "state": self.get_state(),
            "run_log": {
                "starttime": self.starttime,
                "stderr": err,
                "stdour": out
            }
        }

    def get_engine_params(self):
        try:
            return self.request_data['workflow_engine_parameters']
        except:
            return ''

    def get_attachments(self):
        return None

    def get_run_tags(self):
        try:
            return self.request_data['tags']
        except:
            return None

    def get_wf_params(self):
        try:
            return self.request_data['workflow_params']
        except:
            return ''



