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

def GetRunLog(**kwargs):
    return {}


def CancelRun(**kwargs):
    return {}


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
    run = workflow.Workflow(run_id, data)
    runTracker.set_run(run_id, run)

    return {"run_id": run_id}


def GetRunStatus(run_id, **kwargs):
    global runTracker
    run = runTracker.get_run_by_id(run_id)
    return run.get_status()




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
