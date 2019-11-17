
Exploratory work for GA4GH WES and Nextflow.

Based on: https://github.com/common-workflow-language/workflow-service

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

### Checking the status of a workflow
```shell script
curl -X GET --header 'Accept: application/problem+json' \
  'http://127.0.0.1:8080/ga4gh/wes/v1/runs/<RUN ID FROM PREVIOUS STEP>/status'
```