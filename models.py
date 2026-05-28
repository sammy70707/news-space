import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'space.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS planets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            image_url TEXT,
            distance_from_sun TEXT,
            diameter TEXT,
            moons_count INTEGER DEFAULT 0,
            orbital_period TEXT,
            fun_fact TEXT,
            type TEXT DEFAULT 'Terrestrial',
            temperature TEXT,
            gravity TEXT
        );

        CREATE TABLE IF NOT EXISTS satellites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            planet_id INTEGER,
            launch_date TEXT,
            agency TEXT,
            status TEXT DEFAULT 'Active',
            description TEXT NOT NULL,
            image_url TEXT,
            orbit_type TEXT,
            FOREIGN KEY (planet_id) REFERENCES planets(id)
        );

        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            image_url TEXT,
            source_url TEXT,
            published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    conn.commit()
    conn.close()

def create_user(username, email, password_hash):
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_by_username(username):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

def get_user_by_email(email):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user

def get_all_planets():
    conn = get_db()
    planets = conn.execute('SELECT * FROM planets ORDER BY id').fetchall()
    conn.close()
    return planets

def get_planet_by_id(planet_id):
    conn = get_db()
    planet = conn.execute('SELECT * FROM planets WHERE id = ?', (planet_id,)).fetchone()
    conn.close()
    return planet

def get_all_satellites():
    conn = get_db()
    satellites = conn.execute('''
        SELECT s.*, p.name as planet_name
        FROM satellites s
        LEFT JOIN planets p ON s.planet_id = p.id
        ORDER BY s.name
    ''').fetchall()
    conn.close()
    return satellites

def get_satellite_by_id(satellite_id):
    conn = get_db()
    satellite = conn.execute('''
        SELECT s.*, p.name as planet_name
        FROM satellites s
        LEFT JOIN planets p ON s.planet_id = p.id
        WHERE s.id = ?
    ''', (satellite_id,)).fetchone()
    conn.close()
    return satellite

def get_satellites_by_planet(planet_id):
    conn = get_db()
    satellites = conn.execute(
        'SELECT * FROM satellites WHERE planet_id = ? ORDER BY name',
        (planet_id,)
    ).fetchall()
    conn.close()
    return satellites

def get_all_news():
    conn = get_db()
    news = conn.execute('SELECT * FROM news ORDER BY published_at DESC').fetchall()
    conn.close()
    return news

def get_news_by_id(news_id):
    conn = get_db()
    article = conn.execute('SELECT * FROM news WHERE id = ?', (news_id,)).fetchone()
    conn.close()
    return article

def get_latest_news(limit=6):
    conn = get_db()
    news = conn.execute(
        'SELECT * FROM news ORDER BY published_at DESC LIMIT ?', (limit,)
    ).fetchall()
    conn.close()
    return news

def get_news_last_2_weeks():
    conn = get_db()
    news = conn.execute('''
        SELECT * FROM news
        WHERE published_at >= datetime('now', '-14 days')
        ORDER BY published_at DESC
    ''').fetchall()
    conn.close()
    return news

def insert_news_article(title, content, category, image_url, source_url, published_at):
    conn = get_db()
    try:
        existing = conn.execute('SELECT id FROM news WHERE title = ?', (title,)).fetchone()
        if existing:
            conn.close()
            return False
        conn.execute(
            '''INSERT INTO news (title, content, category, image_url, source_url, published_at)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (title, content, category, image_url, source_url, published_at)
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def delete_old_news(days=14):
    conn = get_db()
    conn.execute(
        "DELETE FROM news WHERE published_at < datetime('now', ? || ' days')",
        (f'-{days}',)
    )
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")
