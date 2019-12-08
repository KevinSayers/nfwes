import unittest

from ga4gh.wes.workflow import workflow

class TestWorkflow(unittest.TestCase):
    def test(self):
        request = {
            'workflow_type': 'nextflow',
            'tags': 'testing',
            'workflow_url': 'file:///home/kevin/worknfwes/main.nf',
            'workflow_params': '--message'
        }

        run_id = 1000

        wf = workflow.Workflow(run_id, request)
        self.assertIsInstance(wf, workflow.Workflow)

