from datetime import datetime
from ga4gh.wes.utils.dbconfig import db, ma

class Run(db.Model):
    __tablename__ = "runs"
    run_id = db.Column(db.String, primary_key=True)
    run_dir = db.Column(db.String)
    starttime = db.Column(db.String)
    cmd = db.Column(db.String)
    tags = db.Column(db.String)
    engine_params = db.Column(db.String)



class RunSchema(ma.ModelSchema):
    class Meta:
        model = Run
        sqla_session = db.session


