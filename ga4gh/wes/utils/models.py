from datetime import datetime
from dbconfig import db, ma

class Run(db.Model):
    __tablename__ = "runs"
    run_id = db.Column(db.String, primary_key=True)
    run_dir = db.Column()
    starttime = db.Column(db.String())
    cmd = db.String()
    tags = db.String()
    engine_params = db.String()
    


    # timestamp = db.Column(
    #     db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    # )

    # self.run_id = run_id
    # self.run_dir = self.setup_rundir()
    # self.request_data = request_data
    # self.request_files = request_files
    # self.starttime = datetime.now()
    # self.engine_params = self.get_engine_params()
    # self.workflow_params = self.get_wf_params()
    # self.cmd = None
    # self.run_obj = None
    # self.tags = self.get_run_tags()


class PersonSchema(ma.ModelSchema):
    class Meta:
        model = Run
        sqla_session = db.session


