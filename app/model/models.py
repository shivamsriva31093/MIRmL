from app import db


class Learner(db.Model):
    __tablename__ = 'learner_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    path = db.Column(db.String(1000), unique=True)

    def __repr__(self):
        return '<Learner %r>' % self.name


class Predictor(db.Model):
    __tablename__ = 'predictor_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    path = db.Column(db.String(1000), unique=True)

    def __repr__(self):
        return '<Predictor %r>' % self.track_id


class Temp(db.Model):
    __tablename__ = 'temp_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    track_id = db.Column(db.String(100))
    track = db.Column(db.String(100), unique=True)
    label = db.Column(db.String(10), nullable=False, default='None')
    artist = db.Column(db.String(100), unique=True)
    path = db.Column(db.String(1000), unique=True)

    def __repr__(self):
        return '<Temp %r>' % self.track_id
