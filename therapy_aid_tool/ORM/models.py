from . import db


class Video(db.Model):
    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True)
    filepath = db.Column(db.Text)
    closeness = db.Column(db.Text)
    interactions = db.Column(db.Text)
    interactions_statistics = db.Column(db.Text)
    sessions = db.relationship("Session", lazy="dynamic", backref="videos")

    def __init__(self, **kwargs):
        super(Video, self).__init__(**kwargs)

    def __repr__(self):
        return f"Video(filepath='{self.filepath}', closeness='{self.closeness}', interactions='{self.interactions}', interactions_statistics='{self.interactions_statistics}')"


class Toddler(db.Model):
    __tablename__ = "toddlers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    sessions = db.relationship("Session", lazy="dynamic", backref="toddlers")

    def __init__(self, **kwargs):
        super(Toddler, self).__init__(**kwargs)

    def __repr__(self):
        return f"Toddler(name='{self.name}')"


class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    toddler_id = db.Column(db.Integer, db.ForeignKey("toddlers.id"))
    video_id = db.Column(db.Integer, db.ForeignKey("videos.id"))

    def __init__(self, **kwargs):
        super(Session, self).__init__(**kwargs)

    def __repr__(self):
        return f"Session(name='{self.name}')"
