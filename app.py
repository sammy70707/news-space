from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import models
import news_fetcher
import os

app = Flask(__name__)
app.secret_key = 'space-explorer-secret-key-2026'

_news_fetched = False




def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated




@app.route('/')
def index():
    return render_template('loader.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = models.get_user_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if not username or not email or not password:
            flash('All fields are required', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
        elif password != confirm:
            flash('Passwords do not match', 'error')
        elif models.get_user_by_username(username):
            flash('Username already exists', 'error')
        elif models.get_user_by_email(email):
            flash('Email already registered', 'error')
        else:
            pw_hash = generate_password_hash(password)
            if models.create_user(username, email, pw_hash):
                user = models.get_user_by_username(username)
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('home'))
            flash('An error occurred. Please try again.', 'error')
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    global _news_fetched
    if not _news_fetched:
        import threading
        threading.Thread(target=news_fetcher.refresh_news, daemon=True).start()
        _news_fetched = True

    news = models.get_latest_news(limit=6)
    planets = models.get_all_planets()
    return render_template('home.html', news=news, planets=planets)


@app.route('/news')
@login_required
def news_page():
    news = models.get_news_last_2_weeks()
    return render_template('news.html', news=news)


@app.route('/planets')
@login_required
def planets():
    all_planets = models.get_all_planets()
    return render_template('planets.html', planets=all_planets)


@app.route('/planets/<int:planet_id>')
@login_required
def planet_detail(planet_id):
    planet = models.get_planet_by_id(planet_id)
    if not planet:
        return redirect(url_for('planets'))
    satellites = models.get_satellites_by_planet(planet_id)
    return render_template('planet_detail.html', planet=planet, satellites=satellites)


@app.route('/satellites')
@login_required
def satellites():
    all_satellites = models.get_all_satellites()
    return render_template('satellites.html', satellites=all_satellites)


@app.route('/satellites/<int:satellite_id>')
@login_required
def satellite_detail(satellite_id):
    satellite = models.get_satellite_by_id(satellite_id)
    if not satellite:
        return redirect(url_for('satellites'))
    return render_template('satellite_detail.html', satellite=satellite)


@app.route('/tracker')
@login_required
def tracker():
    all_satellites = models.get_all_satellites()
    return render_template('tracker.html', satellites=all_satellites)


@app.route('/solar-tracker')
@login_required
def solar_tracker():
    all_satellites = models.get_all_satellites()
    return render_template('solar_tracker.html', satellites=all_satellites)


@app.route('/iss-live')
@login_required
def iss_live():
    return render_template('iss_live.html')



if __name__ == '__main__':
    models.init_db()
    news_fetcher.start_background_fetcher()
    news_fetcher.refresh_news()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)