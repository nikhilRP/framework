from app import db


class Sample(db.Model):
    __tablename__ = 'sample'

    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    height = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String, nullable=True)

    def __init__(self, station):
        self.id = station['id']
        self.lon = station['lon']
        self.lat = station['lat']
        self.height = station['height']
        self.name = station['name']

    def __repr__(self):
        return '<id {}>'.format(self.id)
