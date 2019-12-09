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
        self.engine_params = self.get_engine_params()
        self.workflow_params = self.get_wf_params()
        self.cmd = None
        self.run_obj = None
        self.tags = self.get_run_tags()


    def run(self):
        self.cmd = self.get_cmd()
        print (self.cmd)
        process = Popen(self.cmd,
                        cwd=self.run_dir,
                        stdout=PIPE,
                        stderr=PIPE)
        self.run_obj = process

    def runnable_url(self, url):
        if 'https://' in url:
            return url
        if 'file://' in url:
            os.symlink(url[7:], os.path.join(self.run_dir, "nfwes.nf"))
            return os.path.join(self.run_dir, "nfwes.nf")


    def setup_rundir(self):
        Path(f'{Path.cwd()}/runs/{self.run_id}').mkdir(parents=True, exist_ok=True)
        return (f'{Path.cwd()}/runs/{self.run_id}')

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
            "request": self.request_data,
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
            return None

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
            return None

    def get_cmd(self) -> list:
        data = self.request_data
        wf_url = self.runnable_url(data['workflow_url'])

        cmd_list = ['nextflow',
                    'run',
                    wf_url
                    ]
        if self.workflow_params is not None:
            cmd_list.append(self.workflow_params)
        if self.engine_params is not None:
            cmd_list.append(self.engine_params)

        return cmd_list




