from ga4gh.wes.utils import models
from ga4gh.wes.utils.dbconfig import db


db.create_all()
db.session.commit()

