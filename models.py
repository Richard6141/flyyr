from flask_sqlalchemy import SQLAlchemy


from flask import Flask

app=Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String())
    state = db.Column(db.String())
    address = db.Column(db.String())
    phone = db.Column(db.String())
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String())
    facebook_link = db.Column(db.String())
    website_link = db.Column(db.String())
    seeking_description = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
    shows = db.relationship('Show',backref='venues',lazy=True)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String())
    state = db.Column(db.String())
    address = db.Column(db.String())
    phone = db.Column(db.String())
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String())
    facebook_link = db.Column(db.String())
    website_link = db.Column(db.String())
    seeking_description = db.Column(db.String())
    seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
    shows = db.relationship('Show',backref='artists',lazy=True)


    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    
class Show(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'),nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'),nullable=False)
  start_time = db.Column(db.String())
