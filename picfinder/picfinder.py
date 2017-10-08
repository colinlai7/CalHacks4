import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , picfinder.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'picfinder.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('PICFINDER_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select imgname, first from entries')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (imgname, first, second, third, fourth, fifth) values (?,?,?,?,?,?)',
                 [request.form['title'],request.form['text'],request.form['text'],request.form['text'],request.form['text'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        db = get_db()
        name = request.form('filename')
        data = request.form('image')
        features = analyzeImage(data)
        db.execute('insert into entries (imgname, img, first, second, third, fourth, fifth) values (?,?,?,?,?,?,?)',
            [name, data, features[0], features[1], features[2], features[3], features[4]])
            db.commit()
        flash('The image was successfully uploaded!')
        return redirect(url_for('show_entries'))

    if request.method == 'GET':
        return render_template('upload.html')

@app.route('/search', methods=['POST'])
def search():
    db = get_db()

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select imgname, first from entries')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)




#Utility function. Given an image, send it to be analyzed by Google.
#Return a list of 5 features, with most likely in the front and least likely in the back.
def analyzeImage(image):