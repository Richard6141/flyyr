#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from dateutil import parser
from models import db, app, Venue, Artist, Show
from datetime import date
import json
import os
import sys
from this import d
from unicodedata import name
from unittest import result
# from tkinter import Y
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

# def format_datetime(value, format='medium'):
#   date = dateutil.parser.parse(value)
#   if format == 'full':
#       format="EEEE MMMM, d, y 'at' h:mma"
#   elif format == 'medium':
#       format="EE MM, dd, y h:mma"
#   return babel.dates.format_datetime(date, format, locale='en')

# app.jinja_env.filters['datetime'] = format_datetime
def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

def arrange_city_venue(datas, cities):
    areas = []
    for city in cities:
        results = []
        for data in datas:
            if city == data.city:
                results.append(data)
        areas.append({
            "city": city,
            "state": results[0].state,
            "venues": results})
    return areas


@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

    data = Venue.query.all()
    data1 = db.session.query(Venue.city).distinct().all()
    cities = [Cities.city for Cities in data1]
    return render_template('pages/venues.html', areas=arrange_city_venue(data, cities))

# @app.route('/venues')
# def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    # data=[{
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "venues": [{
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "num_upcoming_shows": 0,
    #   }, {
    #     "id": 3,
    #     "name": "Park Square Live Music & Coffee",
    #     "num_upcoming_shows": 1,
    #   }]
    # }, {
    #   "city": "New York",
    #   "state": "NY",
    #   "venues": [{
    #     "id": 2,
    #     "name": "The Dueling Pianos Bar",
    #     "num_upcoming_shows": 0,
    #   }]
    # }]
    # data = []
    # venues = Venue.query.order_by(Venue.state).all()
    # for venue in venues:
    #   total_venue ={
    #     'id': venue.id,
    #     'name': venue.name,
    #   }
    #   if data == []:
    #     pass
    #   else:
    #     ancien = data[len(data)-1]
    #     if ancien['city'] == venue.city and ancien['state'] == venue.state:
    #       ancien[venues].append(total_venue)
    #       continue
    #   data.append({
    #     'city': venue.city,
    #     'state': venue.state,
    #     'venues': [total_venue]
    #   })
    # return render_template('pages/venues.html', areas=data);


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '').strip()
    results = Venue.query.filter(Venue.name.ilike('%'+search_term + '%')).all()
    response = {
        "count": 0,
        "data": []
    }
    for venue in results:
        response["count"] += 1
        response["data"].append({
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': 0,
        })
    # response={
    #   "count": 1,
    #   "data": [{
    #     "id": 2,
    #     "name": "The Dueling Pianos Bar",
    #     "num_upcoming_shows": 0,
    #   }]
    # }

    return render_template('pages/search_venues.html', results=response, search_term=search_term)


# @app.route('/venues/<int:venue_id>')
# def show_venue(venue_id):
#     # shows the venue page with the given venue_id
#     # TODO: replace with real venue data from the venues table, using venue_id
#     # data1={
#     #   "id": 1,
#     #   "name": "The Musical Hop",
#     #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
#     #   "address": "1015 Folsom Street",
#     #   "city": "San Francisco",
#     #   "state": "CA",
#     #   "phone": "123-123-1234",
#     #   "website": "https://www.themusicalhop.com",
#     #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
#     #   "seeking_talent": True,
#     #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
#     #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
#     #   "past_shows": [{
#     #     "artist_id": 4,
#     #     "artist_name": "Guns N Petals",
#     #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#     #     "start_time": "2019-05-21T21:30:00.000Z"
#     #   }],
#     #   "upcoming_shows": [],
#     #   "past_shows_count": 1,
#     #   "upcoming_shows_count": 0,
#     # }
#     # data2={
#     #   "id": 2,
#     #   "name": "The Dueling Pianos Bar",
#     #   "genres": ["Classical", "R&B", "Hip-Hop"],
#     #   "address": "335 Delancey Street",
#     #   "city": "New York",
#     #   "state": "NY",
#     #   "phone": "914-003-1132",
#     #   "website": "https://www.theduelingpianos.com",
#     #   "facebook_link": "https://www.facebook.com/theduelingpianos",
#     #   "seeking_talent": False,
#     #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
#     #   "past_shows": [],
#     #   "upcoming_shows": [],
#     #   "past_shows_count": 0,
#     #   "upcoming_shows_count": 0,
#     # }
#     # data3={
#     #   "id": 3,
#     #   "name": "Park Square Live Music & Coffee",
#     #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
#     #   "address": "34 Whiskey Moore Ave",
#     #   "city": "San Francisco",
#     #   "state": "CA",
#     #   "phone": "415-000-1234",
#     #   "website": "https://www.parksquarelivemusicandcoffee.com",
#     #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
#     #   "seeking_talent": False,
#     #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#     #   "past_shows": [{
#     #     "artist_id": 5,
#     #     "artist_name": "Matt Quevedo",
#     #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
#     #     "start_time": "2019-06-15T23:00:00.000Z"
#     #   }],
#     #   "upcoming_shows": [{
#     #     "artist_id": 6,
#     #     "artist_name": "The Wild Sax Band",
#     #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#     #     "start_time": "2035-04-01T20:00:00.000Z"
#     #   }, {
#     #     "artist_id": 6,
#     #     "artist_name": "The Wild Sax Band",
#     #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#     #     "start_time": "2035-04-08T20:00:00.000Z"
#     #   }, {
#     #     "artist_id": 6,
#     #     "artist_name": "The Wild Sax Band",
#     #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#     #     "start_time": "2035-04-15T20:00:00.000Z"
#     #   }],
#     #   "past_shows_count": 1,
#     #   "upcoming_shows_count": 1,
#     # }

#     # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
#     data = Venue.query.get(venue_id)
#     return render_template('pages/show_venue.html', venue=data)

def getShows(venue):
    shows = Show.query.filter_by(venue_id=venue.id).all()
    past_shows = []
    upcoming_shows = []
    for s in shows:
        if s.start_time >= datetime.now():
            upcoming_shows.append(s)
        past_shows.append(past_shows)
    v = venue.__dict__
    v['past_shows'] = past_shows
    v['upcoming_shows'] = upcoming_shows
    v['upcoming_shows_count'] = len(upcoming_shows)
    v['past_shows_count'] = len(past_shows)
    return v


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    # data1={
    #   "id": 1,
    #   "name": "The Musical Hop",
    #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #   "address": "1015 Folsom Street",
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "phone": "123-123-1234",
    #   "website": "https://www.themusicalhop.com",
    #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
    #   "seeking_talent": True,
    #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #   "past_shows": [{
    #     "artist_id": 4,
    #     "artist_name": "Guns N Petals",
    #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #     "start_time": "2019-05-21T21:30:00.000Z"
    #   }],
    #   "upcoming_shows": [],
    #   "past_shows_count": 1,
    #   "upcoming_shows_count": 0,
    # }
    # data2={
    #   "id": 2,
    #   "name": "The Dueling Pianos Bar",
    #   "genres": ["Classical", "R&B", "Hip-Hop"],
    #   "address": "335 Delancey Street",
    #   "city": "New York",
    #   "state": "NY",
    #   "phone": "914-003-1132",
    #   "website": "https://www.theduelingpianos.com",
    #   "facebook_link": "https://www.facebook.com/theduelingpianos",
    #   "seeking_talent": False,
    #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    #   "past_shows": [],
    #   "upcoming_shows": [],
    #   "past_shows_count": 0,
    #   "upcoming_shows_count": 0,
    # }

    # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2]))[0]

    data = Venue.query.filter_by(id=venue_id)
    res = []
    for dat in data:
        res.append(getShows(dat))
    return render_template('pages/show_venue.html', venue=res[0])

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    error = False
    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        address = request.form.get('address')
        phone = request.form.get('phone')
        image_link = request.form.get('image_link')
        genres = request.form.getlist('genres')
        facebook_link = request.form.get('facebook_link')
        website_link = request.form.get('website_link')
        seeking_description = request.form.get('seeking_description')
        seeking_talent = request.form.get('seeking_talent')

        if seeking_talent == 'y':
            seeking_talent = True

        data = Venue(
            name=name,
            city=city,
            state=state,
            address=address,
            phone=phone,
            image_link=image_link,
            genres=genres,
            facebook_link=facebook_link,
            website_link=website_link,
            seeking_description=seeking_description,
            seeking_talent=seeking_talent,
        )
        db.session.add(data)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        os.abort()
    else:
        #   return jsonify(body)
        # # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    error = False

    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('Une erreur est survenue !')
    else:
        flash('Venue supprimé avec succès !')
    # try:
    #   venue = Venue.query.get(venue_id)
    #   db.session.delete(venue)
    #   db.session.commit()
    # except:
    #   error = True
    #   db.session.rollback()
    #   print(sys.exc_info())
    # finally:
    #   db.session.close()
    # if error:
    #   os.abort ()
    # else:
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
        # return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    # data=[{
    #   "id": 4,
    #   "name": "Guns N Petals",
    # }, {
    #   "id": 5,
    #   "name": "Matt Quevedo",
    # }, {
    #   "id": 6,
    #   "name": "The Wild Sax Band",
    # }]
    return render_template('pages/artists.html', artists=Artist.query.all())


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '').strip()
    results = Artist.query.filter(
        Artist.name.ilike('%'+search_term + '%')).all()
    response = {
        "count": 0,
        "data": []
    }
    for artist in results:
        response["count"] += 1
        response["data"].append({
            'id': artist.id,
            'name': artist.name,
            'num_upcoming_shows': 0,
        })
    # response={
    #   "count": 1,
    #   "data": [{
    #     "id": 4,
    #     "name": "Guns N Petals",
    #     "num_upcoming_shows": 0,
    #   }]
    # }
    return render_template('pages/search_artists.html', results=response, search_term=search_term)


# @app.route('/artists/<int:artist_id>')
# def show_artist(artist_id):
#     # shows the artist page with the given artist_id
#     # TODO: replace with real artist data from the artist table, using artist_id
#     # data1={
#     #   "id": 4,
#     #   "name": "Guns N Petals",
#     #   "genres": ["Rock n Roll"],
#     #   "city": "San Francisco",
#     #   "state": "CA",
#     #   "phone": "326-123-5000",
#     #   "website": "https://www.gunsnpetalsband.com",
#     #   "facebook_link": "https://www.facebook.com/GunsNPetals",
#     #   "seeking_venue": True,
#     #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
#     #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#     #   "past_shows": [{
#     #     "venue_id": 1,
#     #     "venue_name": "The Musical Hop",
#     #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
#     #     "start_time": "2019-05-21T21:30:00.000Z"
#     #   }],
#     #   "upcoming_shows": [],
#     #   "past_shows_count": 1,
#     #   "upcoming_shows_count": 0,
#     # }
#     # data2={
#     #   "id": 5,
#     #   "name": "Matt Quevedo",
#     #   "genres": ["Jazz"],
#     #   "city": "New York",
#     #   "state": "NY",
#     #   "phone": "300-400-5000",
#     #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
#     #   "seeking_venue": False,
#     #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
#     #   "past_shows": [{
#     #     "venue_id": 3,
#     #     "venue_name": "Park Square Live Music & Coffee",
#     #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#     #     "start_time": "2019-06-15T23:00:00.000Z"
#     #   }],
#     #   "upcoming_shows": [],
#     #   "past_shows_count": 1,
#     #   "upcoming_shows_count": 0,
#     # }
#     # data3={
#     #   "id": 6,
#     #   "name": "The Wild Sax Band",
#     #   "genres": ["Jazz", "Classical"],
#     #   "city": "San Francisco",
#     #   "state": "CA",
#     #   "phone": "432-325-5432",
#     #   "seeking_venue": False,
#     #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#     #   "past_shows": [],
#     #   "upcoming_shows": [{
#     #     "venue_id": 3,
#     #     "venue_name": "Park Square Live Music & Coffee",
#     #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#     #     "start_time": "2035-04-01T20:00:00.000Z"
#     #   }, {
#     #     "venue_id": 3,
#     #     "venue_name": "Park Square Live Music & Coffee",
#     #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#     #     "start_time": "2035-04-08T20:00:00.000Z"
#     #   }, {
#     #     "venue_id": 3,
#     #     "venue_name": "Park Square Live Music & Coffee",
#     #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#     #     "start_time": "2035-04-15T20:00:00.000Z"
#     #   }],
#     #   "past_shows_count": 0,
#     #   "upcoming_shows_count": 3,
#     # }
#     artist = Artist.query.filter_by(id=artist_id).first_or_404()
#     # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
#     return render_template('pages/show_artist.html', artist=artist)

@app.route('/artists/<int:id>')
def show_artist(id):
  data = Artist.query.get_or_404(id)

  shows = db.session.query(Show).filter_by(artist_id=id).all()
  past_shows = []
  past_shows_data = []

  upcoming_shows = []
  upcoming_show_data = []
  
  for show in shows:
      if parser.parse(show.start_time) <= datetime.now():
          past_shows.append(show)
      if datetime.timestamp(parser.parse(show.start_time)) > datetime.timestamp(datetime.now()):
          upcoming_shows.append(show)

  for show in past_shows:
      # print(show.venue_id)
      venue = Venue.query.get(show.venue_id)
      
      d = {
          'venue_id': venue.id,
          'venue_name': venue.name,
          'venue_image_link': venue.image_link, 
          "start_time": show.start_time
      }
      past_shows_data.append(d)


  for show in upcoming_shows:
      # print(show.venue_id)
      venue = Venue.query.get(show.venue_id)
      
      d = {
          'venue_id': venue.id,
          'venue_name': venue.name,
          'venue_image_link': venue.image_link, 
          "start_time": show.start_time
      }
      upcoming_show_data.append(d)

  resultat = {
      "id": data.id,
      "name": data.name,
      "genres": data.genres,
      "city": data.city,
      "state": data.state,
      "phone": data.phone,
      "seeking_venue": data.seeking_venue,
      "image_link": data.image_link,
      "past_shows": past_shows_data,
      "upcoming_shows": upcoming_show_data,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows),
  }
  print(resultat)
  return render_template('pages/show_artist.html', artist=resultat)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()

    # TODO: populate form with fields from artist with ID <artist_id>
    artist = Artist.query.filter_by(id=artist_id).first_or_404()
    return render_template('forms/edit_artist.html', form=form, artist=artist)
    # return render_template('forms/edit_artist.html', form=form, artist=Artist.query.get(id).one_or_none())


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    error = False
    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        phone = request.form.get('phone')
        image_link = request.form.get('image_link')
        genres = request.form.getlist('genres')
        facebook_link = request.form.get('facebook_link')
        website_link = request.form.get('website_link')
        seeking_venue = request.form.get('seeking_venue')
        seeking_description = request.form.get('seeking_description')

        # Get the current artist record

        artist = Artist.query.get(artist_id)

        # Update the artist record

        artist.name = name
        artist.city = city
        artist.state = state
        artist.phone = phone
        artist.image_link = image_link
        artist.genres = genres
        artist.facebook_link = facebook_link
        artist.website_link = website_link
        artist.seeking_description = seeking_description
        if request.form.get('seeking_venue') == 'y':
            artist.seeking_venue = True
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('Error: Une erreur est survenue !')
    else:
        return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    # venue={
    #   "id": 1,
    #   "name": "The Musical Hop",
    #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #   "address": "1015 Folsom Street",
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "phone": "123-123-1234",
    #   "website": "https://www.themusicalhop.com",
    #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
    #   "seeking_talent": True,
    #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    # }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=Venue.query.filter_by(id=venue_id).first_or_404())

# @app.route('/venues/<int:venue_id>/edit', methods=['POST'])
# def edit_venue_submission(venue_id):
#   # TODO: take values from the form submitted, and update existing
#   # venue record with ID <venue_id> using the new attributes
#   error = False
#   try:
#     name = request.form['name']
#     city = request.form['city']
#     state = request.form['state']
#     address = request.form['address']
#     phone = request.form['phone']
#     image_link = request.form['image_link']
#     genres = request.form.getlist('genres')
#     facebook_link = request.form['facebook_link']
#     website_link = request.form['website_link']
#     seeking_talent = request.form['seeking_talent']
#     seeking_description = request.form['seeking_description']

#     if seeking_talent == 'y':
#         seeking_talent = True
#     #Get the current Venue record

#     venue = Venue.query.get(venue_id)

#     #Update the venue record

#     venue.name = name
#     venue.city = city
#     venue.state = state
#     venue.phone = phone
#     venue.image_link = image_link
#     venue.genres = genres
#     venue.facebook_link = facebook_link
#     venue.website_link = website_link
#     venue.seeking_talent = seeking_talent
#     venue.seeking_description = seeking_description
#     db.session.commit()
#   except:
#     error = True
#     db.session.rollback()
#     print(sys.exc_info())
#   finally:
#     db.session.close()
#   if error:
#     flash( 'Error: Une erreur est survenue !')
#   else:
#     return redirect(url_for('show_venue', venue_id=venue_id))


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with venue_id <venue_venue_id> using the new attributes
    error = False

    venue = Venue.query.get_or_404(venue_id)

    if request.form.get('seeking_talent') == 'y':
        venue.seeking_talent = True

    venue.name = request.form.get('name')
    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.phone = request.form.get('phone')
    venue.image_link = request.form.get('image_link')
    venue.genres = request.form.getlist('genres')
    venue.facebook_link = request.form.get('facebook_link')

    venue.website_link = request.form.get('website_link')
    venue.seeking_description = request.form.get('seeking_description')

    try:
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Venue ' +
                  request.form['name'] + ' could not be updated.')
        else:
            flash('Venue ' + request.form['name'] +
                  ' was successfully updated!')
        return redirect(url_for('show_venue', venue_id=venue_id))
#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    error = False
    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        address = request.form.get('address')
        phone = request.form.get('phone')
        image_link = request.form.get('image_link')
        genres = request.form.getlist('genres')
        facebook_link = request.form.get('facebook_link')
        website_link = request.form.get('website_link')
        seeking_description = request.form.get('seeking_description')
        seeking_venue = request.form.get('seeking_venue')

        if seeking_venue == 'y':
            seeking_venue = True

        artist = Artist(
            name=name,
            city=city,
            state=state,
            phone=phone,
            image_link=image_link,
            genres=genres,
            address=address,
            facebook_link=facebook_link,
            website_link=website_link,
            seeking_venue=seeking_venue,
            seeking_description=seeking_description
        )
        db.session.add(artist)
        db.session.commit()
        # body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        if request.form['name'] == '':
            error = 'Field name is required'
    finally:
        db.session.close()

    # if error:
    #     os.abort()
    if request.form['phone'] == "":
        flash('Field name is required')
    else:
        #   return jsonify(body)
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html', error=error)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    # data = db.session.query(Show).join(Artist).with_entities(Show.artist_id, Artist.name, Artist.image_link, Show.start_time).filter(Show.venue_id == Venue.id).all()
    data = db.session.query(Show.start_time.label('start_time'),
                            Artist.name.label('artist_name'),
                            Artist.id.label('artist_id'),
                            Artist.image_link.label('artist_image_link'),
                            Venue.id.label('venue_id'), Venue.name.label('venue_name')).join(Artist, Artist.id == Show.artist_id).join(Venue, Venue.id == Show.venue_id).all()
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    error = False
    try:
        artist_id = request.form['artist_id'],
        venue_id = request.form['venue_id'],
        start_time = request.form['start_time'],

        show = Show(artist_id=artist_id, venue_id=venue_id,
                    start_time=start_time)
        db.session.add(show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('Error: Une erreur est survenue !')
    else:
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    app.config['FLASK_DEBUG'] = True
