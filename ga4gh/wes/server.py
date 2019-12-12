import connexion
from flask_cors import CORS
from ga4gh.wes.workflow import workflow
import json
import uuid


class Runs():
    def __init__(self):
        self.runs_dict = {}
        self.counter = 0

    def set_run(self, run_id, run_obj):
        self.runs_dict[run_id] = run_obj

    def get_runs(self):
        return self.runs_dict

    def get_run_by_id(self, run_id):
        return self.runs_dict[run_id]

def GetRunLog(run_id, **kwargs):
    global runTracker
    run = runTracker.get_run_by_id(run_id)
    return run.get_status()


def CancelRun(run_id, **kwargs):
    global runTracker
    r = None

    run = runTracker.get_run_by_id(run_id)
    state = run.get_status()['state']
    if state is 'RUNNING':
        r = {
            'msg': 'The workflow has been cancelled',
            'status_code': 200
        }
    else:
        r = {
            'msg': 'The workflow cannot be cancelled as it is not in the RUNNING state',
            'status_code': 500
        }

    return r



def ListRuns(**kwargs):
    global runTracker
    runs_list = []

    for i in runTracker.get_runs():
        runs_list.append({"run_id": i})

    r = {'runs': runs_list}

    return json.dumps(r)


def GetServiceInfo(**kwargs):
    r = {
        "workflow_type_versions": {
            "Nextflow": {"workflow_type_version": ["v1.0"]}
        },
        "supported_wes_versions": ["1.0.0"],
        "supported_filesystem_protocols": ["file"],
        "workflow_engine_versions": {
            "Nextflow": ["19.07"]
        },
        "system_state_counts": {},
        "tags": {}
    }

    return r

def RunWorkflow(**kwargs):
    global runTracker
    run_id = uuid.uuid4().hex[:5]
    data = connexion.request.form.to_dict(flat=True)

    if data['workflow_type'] == 'nextflow':
        run = workflow.Workflow(run_id, data)
        runTracker.set_run(run_id, run)
        run.run()
        return {"run_id": run_id}
    else:
        return {
            "msg": "This WES only supports submission of workflow_type=nextflow",
            "status_code": 500
        }


def GetRunStatus(run_id, **kwargs):
    global runTracker
    run = runTracker.get_run_by_id(run_id)
    return {
        "run_id": run_id,
        "state": run.get_state()
    }




def configure_app():
    SWAGGER_FILENAME = 'api/workflow_execution_service.swagger.yaml'
    app = connexion.App(
        "ga4gh.wes.server",
        options={"swagger_ui": True})
    app.add_api(SWAGGER_FILENAME)

    CORS(app.app)
    return app



runTracker = Runs()

def main():
    app = configure_app()
    app.run(port=8080, debug=True)


if __name__ == '__main__':
    main()
