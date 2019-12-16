
Exploratory work for GA4GH WES and Nextflow.

Based on: https://github.com/common-workflow-language/workflow-service

| Parameter                  | required   | input     | type          |
| -------------------------- | :--------: | --------- | ------------: |
| workflow_params            | optional   | formData  | string        |
| workflow_type              | optional   | formData  | string        |
| workflow_type_version      | optional   | formData  | string        |
| tags                       | optional   | formData  | string        |
| workflow_engine_parameters | optional   |	formData  |	string        |
| workflow_url               | required   |	formData  | string        |
| workflow_attachment        | optional   | formData  | Array[string] |

# Usage

```shell script
git clone https://github.com/KevinSayers/nfwes
cd nfwes
pip install -r requirements.txt
python ga4gh/wes/server.py
```

### Getting service info
```shell script
curl -X GET --header 'Accept: application/json' \
  'http://127.0.0.1:8080/ga4gh/wes/v1/service-info'
```

### Running a workflow
```shell script
curl -X POST --header 'Content-Type: multipart/form-data' \
  --header 'Accept: application/problem+json' \
  -F workflow_type=nextflow \
  -F workflow_url=https://github.com/nextflow-io/hello \
  'http://127.0.0.1:8080/ga4gh/wes/v1/runs'
```

### Running a workflow with a file attachment
This can be used to attach files such as a config file. This file will be automatically staged in the run directory. 
```shell script
curl -X POST --header 'Content-Type: multipart/form-data' \
  --header 'Accept: application/problem+json' \
  -F workflow_type=nextflow \
  -F workflow_attachment=@<Absolute path to demo folder>/nextflow.config  \
  -F workflow_url=file://<Absolute path to demo folder>/main.nf \   
  'http://127.0.0.1:8080/ga4gh/wes/v1/runs'

```
### Checking the status of a workflow
```shell script
curl -X GET --header 'Accept: application/problem+json' \
  'http://127.0.0.1:8080/ga4gh/wes/v1/runs/<RUN ID FROM PREVIOUS STEP>/status'
```