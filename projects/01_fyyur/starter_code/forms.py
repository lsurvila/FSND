from datetime import datetime

import phonenumbers
from flask_wtf import FlaskForm
from phonenumbers import NumberParseException
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, URL, ValidationError, Optional


def validate_phone(self, field):
    error = ValidationError('Invalid phone number.')
    try:
        input_number = phonenumbers.parse(field.data)
        if not (phonenumbers.is_valid_number(input_number)):
            raise error
    except (ValidationError, NumberParseException):
        raise error


genres_data = [
    ('Alternative', 'Alternative'),
    ('Blues', 'Blues'),
    ('Classical', 'Classical'),
    ('Country', 'Country'),
    ('Electronic', 'Electronic'),
    ('Folk', 'Folk'),
    ('Funk', 'Funk'),
    ('Hip-Hop', 'Hip-Hop'),
    ('Heavy Metal', 'Heavy Metal'),
    ('Instrumental', 'Instrumental'),
    ('Jazz', 'Jazz'),
    ('Musical Theatre', 'Musical Theatre'),
    ('Pop', 'Pop'),
    ('Punk', 'Punk'),
    ('R&B', 'R&B'),
    ('Reggae', 'Reggae'),
    ('Rock n Roll', 'Rock n Roll'),
    ('Soul', 'Soul'),
    ('Other', 'Other'),
]


states_data = [
    ('AL', 'AL'),
    ('AK', 'AK'),
    ('AZ', 'AZ'),
    ('AR', 'AR'),
    ('CA', 'CA'),
    ('CO', 'CO'),
    ('CT', 'CT'),
    ('DE', 'DE'),
    ('DC', 'DC'),
    ('FL', 'FL'),
    ('GA', 'GA'),
    ('HI', 'HI'),
    ('ID', 'ID'),
    ('IL', 'IL'),
    ('IN', 'IN'),
    ('IA', 'IA'),
    ('KS', 'KS'),
    ('KY', 'KY'),
    ('LA', 'LA'),
    ('ME', 'ME'),
    ('MT', 'MT'),
    ('NE', 'NE'),
    ('NV', 'NV'),
    ('NH', 'NH'),
    ('NJ', 'NJ'),
    ('NM', 'NM'),
    ('NY', 'NY'),
    ('NC', 'NC'),
    ('ND', 'ND'),
    ('OH', 'OH'),
    ('OK', 'OK'),
    ('OR', 'OR'),
    ('MD', 'MD'),
    ('MA', 'MA'),
    ('MI', 'MI'),
    ('MN', 'MN'),
    ('MS', 'MS'),
    ('MO', 'MO'),
    ('PA', 'PA'),
    ('RI', 'RI'),
    ('SC', 'SC'),
    ('SD', 'SD'),
    ('TN', 'TN'),
    ('TX', 'TX'),
    ('UT', 'UT'),
    ('VT', 'VT'),
    ('VA', 'VA'),
    ('WA', 'WA'),
    ('WV', 'WV'),
    ('WI', 'WI'),
    ('WY', 'WY'),
]


class ShowForm(FlaskForm):
    artist_id = StringField(
        'Artist ID (ID can be found on the Artist\'s Page)', validators=[DataRequired()]
    )
    venue_id = StringField(
        'Venue ID (ID can be found on the Venue\'s Page)', validators=[DataRequired()]
    )
    start_time = DateTimeField(
        'Start Time',
        validators=[DataRequired()],
        default=datetime.today()
    )
    submit = SubmitField('Create Show')


class VenueForm(FlaskForm):
    name = StringField(
        'Name', validators=[DataRequired()]
    )
    city = StringField(
        'City', validators=[DataRequired()]
    )
    state = SelectField(
        'State', validators=[DataRequired()],
        choices=states_data
    )
    address = StringField(
        'Address', validators=[DataRequired()]
    )
    phone = StringField(
        'Phone', validators=[DataRequired(), validate_phone]
    )
    genres = SelectMultipleField(
        'Genres (Ctrl+Click to select multiple)', validators=[DataRequired()],
        choices=genres_data
    )
    website = StringField(
        'Website', validators=[Optional(), URL()]
    )
    facebook_link = StringField(
        'Facebook Link', validators=[Optional(), URL()]
    )
    image_link = StringField(
        'Photo Link', validators=[Optional(), URL()]
    )
    seeking_talent_description = TextAreaField(
        'Message for Artists'
    )
    submit = SubmitField('Create Venue')


class ArtistForm(FlaskForm):
    name = StringField(
        'Name', validators=[DataRequired()]
    )
    city = StringField(
        'City', validators=[DataRequired()]
    )
    state = SelectField(
        'State', validators=[DataRequired()],
        choices=states_data
    )
    phone = StringField(
        'Phone', validators=[DataRequired(), validate_phone]
    )
    genres = SelectMultipleField(
        'Genres (Ctrl+Click to select multiple)', validators=[DataRequired()],
        choices=genres_data
    )
    website = StringField(
        'Website', validators=[Optional(), URL()]
    )
    facebook_link = StringField(
        'Facebook Link', validators=[Optional(), URL()]
    )
    image_link = StringField(
        'Photo Link', validators=[Optional(), URL()]
    )
    seeking_venue_description = TextAreaField(
        'Message for Venues'
    )
    submit = SubmitField('Create Artist')
