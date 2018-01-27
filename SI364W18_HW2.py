## SI 364
## Winter 2018
## HW 2 - Part 1

#Referenced: https://stackoverflow.com/questions/20170234/validate-on-submit-always-returns-false-using-flask-wtforms?rq=1

## This homework has 3 parts, all of which should be completed inside this file.

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################

from flask import Flask, request, render_template, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xxart3mis'

import requests
import json


####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
	choices = [('1','1'),('2','2'),('3','3')]
	albumname = StringField('Enter the name of an album:', validators = [Required()])
	alb_like = RadioField('How much do you like this album? (1 low, 3 high)', choices=choices, validators = [Required()])
	submit = SubmitField('Submit')

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def artistform():
	return render_template('artistform.html')

@app.route('/artistinfo')
def artistinfo():
	r = requests.get('https://itunes.apple.com/search?', params= {'term':request.args['artist']})
	response_dict = json.loads(r.text)
	return render_template('artist_info.html', objects = response_dict['results'])

@app.route('/artistlinks')
def artistlink():
	return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def specificsong(artist_name):
	r2 = requests.get('https://itunes.apple.com/search?', params= {'term':artist_name})
	result = json.loads(r2.text)
	return render_template('specific_artist.html', results = result['results'])

@app.route('/album_entry')
def album_entry():
	simpleform = AlbumEntryForm()
	return render_template('album_entry.html', form = simpleform)

@app.route('/album_result', methods = ['GET', 'POST'])
def album_result():
    form = AlbumEntryForm(request.form)
    if form.validate_on_submit():
	    alb_name = request.form['albumname']
	    likes = request.form['alb_like']
	    return render_template('album_data.html', alb_name = alb_name, rating = likes)
    flash("All Fields Required to Continue!")
    return redirect(url_for('album_entry'))

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)

    
