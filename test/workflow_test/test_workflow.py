import unittest

from ga4gh.wes.workflow import workflow

class TestWorkflow(unittest.TestCase):
    request = {
        'workflow_type': 'nextflow',
        'tags': 'testing',
        'workflow_url': 'https://github.com/nextflow-io/hello',
        'workflow_params': '--message helloworld'
    }

    run_id = 1000
    wf = workflow.Workflow(run_id, request)

    def test_wf_type(self):
        self.assertIsInstance(self.wf, workflow.Workflow)

    def test_get_workflow_params(self):
        self.assertEqual(self.wf.get_wf_params(),
                         ['--message', 'helloworld'])

    def test_cmd(self):
        self.assertEqual(self.wf.get_cmd(),
                         ['nextflow', 'run', 'https://github.com/nextflow-io/hello', '--message', 'helloworld'])

