# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import logging
import os
import sys
from datetime import datetime
from logging import Formatter, FileHandler

import babel
import dateutil.parser
from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import func

from forms import VenueForm, ArtistForm, ShowForm

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
CSRFProtect(app)
Bootstrap(app)
Moment(app)
db = SQLAlchemy(app)
Migrate(app, db)


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Show {self.id}>'


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    website = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(500), nullable=True)
    shows = db.relationship('Show', backref='venue')

    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(120), nullable=True)
    shows = db.relationship('Show', backref='artist')

    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format_param='medium'):
    date = dateutil.parser.parse(value)
    if format_param == 'full':
        format_param = "EEEE MMMM, d, y 'at' h:mma"
    elif format_param == 'medium':
        format_param = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format_param)


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    data = []
    distinct_cities = Venue.query.distinct(Venue.city, Venue.state).all()
    for i in distinct_cities:
        venues_data = []
        venues_in_city = Venue.query.filter_by(city=i.city, state=i.state).all()
        for j in venues_in_city:
            upcoming_shows = get_upcoming_shows(j.shows)
            venues_data.append({
                'id': j.id,
                'name': j.name,
                'num_upcoming_shows': len(upcoming_shows)
            })
        data.append({
            'city': i.city,
            'state': i.state,
            'venues': venues_data
        })
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    query = Venue.query.filter(func.lower(Venue.name).contains(func.lower(search_term)))
    results = query.all()
    count = query.count()
    data = []
    for i in results:
        upcoming_shows = get_upcoming_shows(i.shows)
        data.append({
            "id": i.id,
            "name": i.name,
            "num_upcoming_shows": len(upcoming_shows)
        })
    response = {
        "count": count,
        "data": data
    }
    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    past_shows_data = get_past_shows(venue.shows)
    upcoming_shows_data = get_upcoming_shows(venue.shows)
    past_shows = []
    for i in past_shows_data:
        past_shows.append({
            "artist_id": i.artist.id,
            "artist_name": i.artist.name,
            "artist_image_link": i.artist.image_link,
            "start_time": datetime_to_string(i.start_time)
        })
    upcoming_shows = []
    for i in upcoming_shows_data:
        upcoming_shows.append({
            "artist_id": i.artist.id,
            "artist_name": i.artist.name,
            "artist_image_link": i.artist.image_link,
            "start_time": datetime_to_string(i.start_time)
        })
    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows": upcoming_shows,
        "upcoming_shows_count": len(upcoming_shows)
    }
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    if form.validate_on_submit():
        try:
            venue = Venue(name=form.name.data,
                          city=form.city.data,
                          state=form.state.data,
                          address=form.address.data,
                          phone=form.phone.data,
                          image_link=form.image_link.data if form.image_link.data else None,
                          facebook_link=form.facebook_link.data if form.facebook_link.data else None,
                          genres=form.genres.data,
                          website=form.website.data if form.website.data else None,
                          seeking_talent=True if form.seeking_talent_description.data else False,
                          seeking_description=form.seeking_talent_description.data
                          if form.seeking_talent_description.data else None)
            db.session.add(venue)
            db.session.commit()
            flash('Venue ' + form.name.data + ' was successfully listed!')
            return render_template('pages/home.html')
        except Exception:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
            return render_template('pages/home.html')
        finally:
            db.session.close()
    else:
        return render_template('forms/new_venue.html', form=form)


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = []
    all_artists = Artist.query.all()
    for i in all_artists:
        upcoming_shows = get_upcoming_shows(i.shows)
        data.append({
            "id": i.id,
            "name": i.name,
            "num_upcoming_shows": len(upcoming_shows)
        })
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    query = Artist.query.filter(func.lower(Artist.name).contains(func.lower(search_term)))
    results = query.all()
    count = query.count()
    data = []
    for i in results:
        upcoming_shows = get_upcoming_shows(i.shows)
        data.append({
            "id": i.id,
            "name": i.name,
            "num_upcoming_shows": len(upcoming_shows)
        })
    response = {
        "count": count,
        "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    past_shows_data = get_past_shows(artist.shows)
    upcoming_shows_data = get_upcoming_shows(artist.shows)
    past_shows = []
    for i in past_shows_data:
        past_shows.append({
            "venue_id": i.venue.id,
            "venue_name": i.venue.name,
            "venue_image_link": i.venue.image_link,
            "start_time": datetime_to_string(i.start_time)
        })
    upcoming_shows = []
    for i in upcoming_shows_data:
        upcoming_shows.append({
            "venue_id": i.venue.id,
            "venue_name": i.venue.name,
            "venue_image_link": i.venue.image_link,
            "start_time": datetime_to_string(i.start_time)
        })
    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }
    return render_template('pages/show_artist.html', artist=data)


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    if form.validate_on_submit():
        try:
            artist = Artist(name=form.name.data,
                            city=form.city.data,
                            state=form.state.data,
                            phone=form.phone.data,
                            image_link=form.image_link.data if form.image_link.data else None,
                            facebook_link=form.facebook_link.data if form.facebook_link.data else None,
                            genres=form.genres.data,
                            website=form.website.data if form.website.data else None,
                            seeking_venue=True if form.seeking_venue_description.data else False,
                            seeking_description=form.seeking_venue_description.data
                            if form.seeking_venue_description.data else None)
            db.session.add(artist)
            db.session.commit()
            flash('Artist ' + form.name.data + ' was successfully listed!')
            return render_template('pages/home.html')
        except Exception:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
            return render_template('pages/home.html')
        finally:
            db.session.close()
    else:
        return render_template('forms/new_artist.html', form=form)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = []
    shows_data = Show.query.all()
    for i in shows_data:
        data.append({
            "venue_id": i.venue.id,
            "venue_name": i.venue.name,
            "artist_id": i.artist.id,
            "artist_name": i.artist.name,
            "artist_image_link": i.artist.image_link,
            "start_time": datetime_to_string(i.start_time)
        })
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm()
    if form.validate_on_submit():
        try:
            show = Show(artist_id=form.artist_id.data,
                        venue_id=form.venue_id.data,
                        start_time=form.start_time.data)
            db.session.add(show)
            db.session.commit()
            flash('Show was successfully listed!')
            return render_template('pages/home.html')
        except Exception:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. Show could not be listed.')
            return render_template('pages/home.html')
        finally:
            db.session.close()
    else:
        return render_template('forms/new_show.html', form=form)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


def get_past_shows(shows_data):
    return [i for i in shows_data if i.start_time <= datetime.utcnow()]


def get_upcoming_shows(shows_data):
    return [i for i in shows_data if i.start_time > datetime.utcnow()]


def datetime_to_string(date_time):
    return date_time.strftime("%m/%d/%Y, %H:%M:%S")


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
