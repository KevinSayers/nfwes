from ga4gh.wes.utils.models import Run
from ga4gh.wes.utils.dbconfig import db


db.create_all()

p = Run(run_id='10ada0', run_dir='/test', starttime='2020', cmd="echo hello", tags="what", engine_params="testing")
db.session.add(p)

db.session.commit()

