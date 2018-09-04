from flask_sqlalchemy import SQLAlchemy
import uuid

# create a new SQLAlchemy object
db = SQLAlchemy()

# Base model that for other models to inherit from
class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
            onupdate=db.func.current_timestamp())

# Model for poll topics
class Topics(Base):
    title = db.Column(db.String(500))
    status = db.Column(db.Boolean, default=1) # to mark poll as open or closed should be under title not polls

    # user friendly way to display the object
    def __repr__(self):
        return self.title + ', status: ' + str(self.status) + ', options: ' + str(self.options.all())

    # returns dictionary that can easily be jsonified
    def to_json(self):
        return {
                'title': self.title,
                'options':
                    [{'name': option.option.name, 'vote_count': option.vote_count}
                        for option in self.options.all()],
                'status': self.status
            }

# Model for poll options
class Options(Base):
    name = db.Column(db.String(200), unique=True)

    def __repr__(self):
        return self.name

    def to_json(self):
        return {
                'id': uuid.uuid4(), # Generates a random uuid
                'name': self.name
        }

# Polls model to connect topics and options together
class Polls(Base):

    # Columns declaration
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'))
    vote_count = db.Column(db.Integer, default=0)
    status = db.Column(db.Boolean) # to mark poll as open or closed

    # Relationship declaration (makes it easier for us to access the polls model
    # from the other models it's related to)
    topic = db.relationship('Topics', foreign_keys=[topic_id],
            backref=db.backref('options', lazy='dynamic'))
    option = db.relationship('Options',foreign_keys=[option_id])

    def __repr__(self):
        # a user friendly way to view our objects in the terminal
        return self.option.name

class Users(Base):
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
