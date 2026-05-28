
import sqlite3
import os
from models import get_db, init_db

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'space.db')


def reset_db():

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()


def seed_planets(cursor):
    planets = [
        (
            'Mercury',
            'Mercury is the smallest planet in our solar system and the closest to the Sun. It has a heavily cratered surface similar to Earth\'s Moon. Despite being close to the Sun, it is not the hottest planet due to its lack of atmosphere.',
            '/static/images/mercury.png',
            '57.9 million km', '4,879 km', 0, '88 Earth days',
            'A day on Mercury (sunrise to sunrise) lasts 176 Earth days — longer than its year!',
            'Terrestrial', '-180°C to 430°C', '3.7 m/s²'
        ),
        (
            'Venus',
            'Venus is the second planet from the Sun and the hottest planet in our solar system. Its thick atmosphere traps heat in a runaway greenhouse effect, making it hotter than Mercury. Venus rotates backwards compared to most planets.',
            '/static/images/venus.png',
            '108.2 million km', '12,104 km', 0, '225 Earth days',
            'Venus spins backwards — meaning the Sun rises in the west and sets in the east!',
            'Terrestrial', '462°C (average)', '8.87 m/s²'
        ),
        (
            'Earth',
            'Earth is the third planet from the Sun and the only known planet to harbor life. It has liquid water on its surface, a protective atmosphere, and a magnetic field that shields it from solar radiation.',
            '/static/images/earth.png',
            '149.6 million km', '12,742 km', 1, '365.25 days',
            'Earth is the only planet not named after a Greek or Roman god.',
            'Terrestrial', '-88°C to 58°C', '9.81 m/s²'
        ),
        (
            'Mars',
            'Mars is the fourth planet from the Sun, known as the Red Planet due to iron oxide on its surface. It has the tallest mountain (Olympus Mons) and the deepest canyon (Valles Marineris) in the solar system.',
            '/static/images/mars.png',
            '227.9 million km', '6,779 km', 2, '687 Earth days',
            'Mars has a mountain nearly 3 times the height of Mount Everest — Olympus Mons!',
            'Terrestrial', '-87°C to -5°C', '3.72 m/s²'
        ),
        (
            'Jupiter',
            'Jupiter is the largest planet in our solar system — a gas giant with a mass more than twice that of all other planets combined. Its Great Red Spot is a storm that has been raging for at least 350 years.',
            '/static/images/jupiter.png',
            '778.5 million km', '139,820 km', 95, '11.86 Earth years',
            'Jupiter\'s Great Red Spot is a storm big enough to swallow Earth!',
            'Gas Giant', '-145°C (cloud top)', '24.79 m/s²'
        ),
        (
            'Saturn',
            'Saturn is the sixth planet from the Sun and is best known for its stunning ring system made of ice and rock particles. It is a gas giant with at least 146 known moons.',
            '/static/images/saturn.png',
            '1.434 billion km', '116,460 km', 146, '29.46 Earth years',
            'Saturn is so light it would float if you could find a bathtub big enough!',
            'Gas Giant', '-178°C (cloud top)', '10.44 m/s²'
        ),
        (
            'Uranus',
            'Uranus is the seventh planet from the Sun and is an ice giant. It is unique because it rotates on its side, with an axial tilt of about 98 degrees, effectively rolling around the Sun.',
            '/static/images/uranus.png',
            '2.871 billion km', '50,724 km', 27, '84 Earth years',
            'Uranus rotates on its side like a rolling ball — possibly due to an ancient collision!',
            'Ice Giant', '-224°C', '8.87 m/s²'
        ),
        (
            'Neptune',
            'Neptune is the eighth and farthest planet from the Sun. This ice giant has the strongest winds in the solar system, reaching speeds of 2,100 km/h. It has a vivid blue color due to methane in its atmosphere.',
            '/static/images/neptune.png',
            '4.495 billion km', '49,244 km', 16, '164.8 Earth years',
            'Neptune\'s winds are the fastest in the solar system — over 2,000 km/h!',
            'Ice Giant', '-214°C', '11.15 m/s²'
        ),
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO planets
        (name, description, image_url, distance_from_sun, diameter, moons_count,
         orbital_period, fun_fact, type, temperature, gravity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', planets)


def seed_satellites(cursor):
    planet_ids = {}
    for row in cursor.execute('SELECT id, name FROM planets').fetchall():
        planet_ids[row[0]] = row[1]

    pid = {}
    for row in cursor.execute('SELECT id, name FROM planets').fetchall():
        pid[row[1]] = row[0]

    satellites = [

        (
            'Sputnik 1',
            pid.get('Earth'),
            '1957-10-04', 'Soviet Union (USSR)', 'Completed',
            'Sputnik 1 was the first artificial Earth satellite. Launched by the Soviet Union, this small 58 cm polished metal sphere with four antennas transmitted radio pulses for 21 days, igniting the Space Age and the US-Soviet space race.',
            '/static/images/voyager.png',
            'Low Earth Orbit'
        ),
        (
            'Sputnik 2',
            pid.get('Earth'),
            '1957-11-03', 'Soviet Union (USSR)', 'Completed',
            'Sputnik 2 carried the first living creature into orbit — a dog named Laika. The mission provided data on how living organisms tolerate the space environment, paving the way for human spaceflight.',
            '/static/images/voyager.png',
            'Low Earth Orbit'
        ),
        (
            'Explorer 1',
            pid.get('Earth'),
            '1958-01-31', 'NASA (USA)', 'Completed',
            'Explorer 1 was the first satellite launched by the United States. It discovered the Van Allen radiation belts surrounding Earth, one of the most significant scientific discoveries of the early space age.',
            '/static/images/voyager.png',
            'Low Earth Orbit'
        ),
        (
            'Vanguard 1',
            pid.get('Earth'),
            '1958-03-17', 'NASA (USA)', 'Completed',
            'Vanguard 1 is the oldest satellite still in orbit. It was the first satellite to use solar power. Though no longer functional, it continues to orbit Earth and is expected to remain in orbit for centuries.',
            '/static/images/voyager.png',
            'Medium Earth Orbit'
        ),


        (
            'TIROS-1',
            pid.get('Earth'),
            '1960-04-01', 'NASA (USA)', 'Completed',
            'TIROS-1 (Television Infrared Observation Satellite) was the first successful weather satellite. It proved that satellites could observe Earth\'s weather patterns from space, revolutionizing meteorology forever.',
            '/static/images/hubble.png',
            'Low Earth Orbit'
        ),
        (
            'Telstar 1',
            pid.get('Earth'),
            '1962-07-10', 'AT&T / NASA (USA)', 'Completed',
            'Telstar 1 was the first active communications satellite, relaying the first live transatlantic television signal. It transmitted the first satellite TV pictures, telephone calls, and fax images between the US and Europe.',
            '/static/images/hubble.png',
            'Medium Earth Orbit'
        ),
        (
            'Mariner 2',
            pid.get('Venus'),
            '1962-08-27', 'NASA (USA)', 'Completed',
            'Mariner 2 was the first spacecraft to successfully fly by another planet. It confirmed Venus\'s extremely high surface temperature and dense atmosphere, overturning earlier theories about the planet.',
            '/static/images/voyager.png',
            'Heliocentric (Venus Flyby)'
        ),
        (
            'Syncom 3',
            pid.get('Earth'),
            '1964-08-19', 'NASA (USA)', 'Completed',
            'Syncom 3 was the first geostationary satellite, maintaining a fixed position relative to Earth\'s surface. It broadcast the 1964 Tokyo Olympics live across the Pacific — the first major TV broadcast via satellite.',
            '/static/images/hubble.png',
            'Geostationary Orbit'
        ),
        (
            'Mariner 4',
            pid.get('Mars'),
            '1964-11-28', 'NASA (USA)', 'Completed',
            'Mariner 4 performed the first successful flyby of Mars and returned the first close-up photos of another planet. The 22 images revealed a cratered, seemingly dead world, shocking scientists who expected Earth-like features.',
            '/static/images/mars_orbiter.png',
            'Heliocentric (Mars Flyby)'
        ),
        (
            'Luna 9',
            None,
            '1966-01-31', 'Soviet Union (USSR)', 'Completed',
            'Luna 9 was the first spacecraft to achieve a soft landing on the Moon and transmit photographs from the lunar surface. It proved the surface was solid enough to support a spacecraft, enabling future Moon landings.',
            '/static/images/lunar_orbiter.png',
            'Lunar Surface'
        ),


        (
            'Landsat 1',
            pid.get('Earth'),
            '1972-07-23', 'NASA / USGS (USA)', 'Completed',
            'Landsat 1 was the first Earth-observation satellite designed to study our planet\'s land surfaces. It launched the longest-running program for satellite imagery of Earth, still continuing today with Landsat 9.',
            '/static/images/hubble.png',
            'Sun-Synchronous Orbit'
        ),
        (
            'Pioneer 10',
            pid.get('Jupiter'),
            '1972-03-03', 'NASA (USA)', 'Completed',
            'Pioneer 10 was the first spacecraft to travel through the asteroid belt, the first to make direct observations of Jupiter, and the first to achieve solar system escape velocity. It carried a gold plaque with a message for extraterrestrial life.',
            '/static/images/voyager.png',
            'Heliocentric (Jupiter Flyby)'
        ),
        (
            'Pioneer 11',
            pid.get('Saturn'),
            '1973-04-06', 'NASA (USA)', 'Completed',
            'Pioneer 11 was the first spacecraft to study Saturn up close. After flying past Jupiter, it became the first probe to encounter Saturn, sending back the first close-up images of the ringed planet and discovering a new moon and ring.',
            '/static/images/voyager.png',
            'Heliocentric (Saturn Flyby)'
        ),
        (
            'Skylab',
            pid.get('Earth'),
            '1973-05-14', 'NASA (USA)', 'Completed',
            'Skylab was the United States\' first space station. Three crews lived and worked aboard for a total of 171 days, conducting experiments in solar astronomy, Earth observation, and the effects of microgravity on the human body.',
            '/static/images/iss.png',
            'Low Earth Orbit'
        ),
        (
            'Viking 1',
            pid.get('Mars'),
            '1975-08-20', 'NASA (USA)', 'Completed',
            'Viking 1 was the first spacecraft to successfully land on Mars and perform its mission. Its lander returned the first color photos from the Martian surface, and its biology experiments searched for signs of life.',
            '/static/images/mars_orbiter.png',
            'Mars Surface / Orbit'
        ),
        (
            'Voyager 2',
            None,
            '1977-08-20', 'NASA (USA)', 'Active',
            'Voyager 2 is the only spacecraft to have visited all four giant planets — Jupiter, Saturn, Uranus, and Neptune. Launched in 1977, it is now in interstellar space, still transmitting scientific data from over 20 billion km away.',
            '/static/images/voyager.png',
            'Interstellar Space'
        ),
        (
            'Voyager 1',
            None,
            '1977-09-05', 'NASA (USA)', 'Active',
            'Voyager 1 is the farthest human-made object from Earth. After flyby missions of Jupiter and Saturn, it entered interstellar space in 2012 and continues to send data from over 24 billion km away. It carries the famous Golden Record.',
            '/static/images/voyager.png',
            'Interstellar Space'
        ),


        (
            'Mir Space Station',
            pid.get('Earth'),
            '1986-02-20', 'Soviet Union / Russia', 'Completed',
            'Mir was the first modular space station, assembled in orbit from 1986 to 1996. It served as a continuously inhabited research station for nearly 10 years, setting records for the longest continuous human presence in space.',
            '/static/images/iss.png',
            'Low Earth Orbit'
        ),
        (
            'Hubble Space Telescope',
            pid.get('Earth'),
            '1990-04-24', 'NASA / ESA', 'Active',
            'The Hubble Space Telescope has been one of the most significant instruments in the history of astronomy. Orbiting above Earth\'s atmosphere, it has captured iconic images of deep space including the Pillars of Creation and Hubble Deep Field.',
            '/static/images/hubble.png',
            'Low Earth Orbit'
        ),
        (
            'SOHO',
            None,
            '1995-12-02', 'ESA / NASA', 'Active',
            'The Solar and Heliospheric Observatory (SOHO) has been studying the Sun for over 30 years from the Sun-Earth L1 point. It has discovered over 4,000 comets and provides real-time solar wind data critical for space weather forecasting.',
            '/static/images/hubble.png',
            'Sun-Earth L1 Lagrange Point'
        ),


        (
            'International Space Station (ISS)',
            pid.get('Earth'),
            '1998-11-20', 'NASA / Roscosmos / ESA / JAXA / CSA', 'Active',
            'The ISS is the largest modular space station in low Earth orbit. A joint project among five space agencies, it has been continuously occupied since November 2000 and serves as a microgravity research laboratory for biology, physics, and astronomy.',
            '/static/images/iss.png',
            'Low Earth Orbit'
        ),
        (
            'Chandra X-Ray Observatory',
            pid.get('Earth'),
            '1999-07-23', 'NASA (USA)', 'Active',
            'Chandra is one of NASA\'s Great Observatories, designed to detect X-ray emission from very hot regions of the universe. It has observed black holes, supernovae remnants, and dark matter with unprecedented resolution.',
            '/static/images/hubble.png',
            'Highly Elliptical Orbit'
        ),
        (
            'Mars Odyssey',
            pid.get('Mars'),
            '2001-04-07', 'NASA (USA)', 'Active',
            'Mars Odyssey is the longest-serving spacecraft at Mars. It has mapped the chemical and mineral makeup of the Martian surface, found vast deposits of water ice, and served as a communication relay for Mars rovers.',
            '/static/images/mars_orbiter.png',
            'Mars Orbit'
        ),
        (
            'Mars Exploration Rover — Spirit',
            pid.get('Mars'),
            '2003-06-10', 'NASA (USA)', 'Completed',
            'Spirit (MER-A) landed on Mars in January 2004 for a 90-day mission but lasted over 6 years. It discovered evidence of ancient hot springs and water activity, transforming our understanding of Mars\' wet past.',
            '/static/images/mars_orbiter.png',
            'Mars Surface'
        ),
        (
            'Mars Exploration Rover — Opportunity',
            pid.get('Mars'),
            '2003-07-07', 'NASA (USA)', 'Completed',
            'Opportunity (MER-B) holds the record for the longest Mars surface mission — over 14 years and 45 km traveled (designed for 90 days and 600 meters). It found definitive evidence that water once existed on Mars.',
            '/static/images/mars_orbiter.png',
            'Mars Surface'
        ),
        (
            'Cassini-Huygens',
            pid.get('Saturn'),
            '1997-10-15', 'NASA / ESA / ASI', 'Completed',
            'Cassini orbited Saturn for 13 years (2004–2017), revolutionizing our understanding of the ringed planet. It discovered ocean worlds (Enceladus), methane lakes on Titan, and its Huygens probe became the first to land in the outer solar system.',
            '/static/images/cassini.png',
            'Saturn Orbit'
        ),
        (
            'Mars Reconnaissance Orbiter',
            pid.get('Mars'),
            '2005-08-12', 'NASA (USA)', 'Active',
            'MRO carries the most powerful camera (HiRISE) ever sent to another planet, mapping Mars in extraordinary detail. It has found evidence of seasonal water flows and serves as the primary communication relay for surface missions.',
            '/static/images/mars_orbiter.png',
            'Mars Orbit'
        ),
        (
            'New Horizons',
            None,
            '2006-01-19', 'NASA (USA)', 'Active',
            'New Horizons made history with the first flyby of Pluto in July 2015, revealing a geologically active world with mountains of water ice and a heart-shaped nitrogen glacier. It then visited the Kuiper Belt object Arrokoth in 2019.',
            '/static/images/voyager.png',
            'Heliocentric (Kuiper Belt)'
        ),


        (
            'Kepler Space Telescope',
            pid.get('Earth'),
            '2009-03-07', 'NASA (USA)', 'Completed',
            'Kepler revolutionized exoplanet science, discovering over 2,600 confirmed planets outside our solar system. It revealed that planets are common in our galaxy and that Earth-sized worlds in habitable zones exist around other stars.',
            '/static/images/hubble.png',
            'Earth-trailing Heliocentric'
        ),
        (
            'Lunar Reconnaissance Orbiter',
            None,
            '2009-06-18', 'NASA (USA)', 'Active',
            'LRO has been orbiting the Moon since 2009, creating the most detailed maps of the lunar surface ever made. Its data has identified potential landing sites and water ice deposits crucial for future crewed lunar missions.',
            '/static/images/lunar_orbiter.png',
            'Lunar Orbit'
        ),
        (
            'Curiosity Rover (MSL)',
            pid.get('Mars'),
            '2011-11-26', 'NASA (USA)', 'Active',
            'Curiosity is a car-sized rover exploring Gale Crater on Mars since August 2012. It determined that Mars once had conditions favorable for microbial life, finding ancient riverbeds, organic molecules, and seasonal methane variations.',
            '/static/images/mars_orbiter.png',
            'Mars Surface'
        ),
        (
            'Juno',
            pid.get('Jupiter'),
            '2011-08-05', 'NASA (USA)', 'Active',
            'Juno has been orbiting Jupiter since 2016, studying its atmosphere, magnetic field, and internal structure. It revealed that Jupiter\'s iconic bands extend thousands of km deep and captured stunning close-up images of the planet\'s swirling clouds.',
            '/static/images/juno.png',
            'Jupiter Polar Orbit'
        ),
        (
            'MAVEN',
            pid.get('Mars'),
            '2013-11-18', 'NASA (USA)', 'Active',
            'MAVEN (Mars Atmosphere and Volatile Evolution) studies how Mars lost its atmosphere and water over billions of years. It discovered that solar wind stripped away Mars\' atmosphere, transforming it from a warm, wet world to the cold desert it is today.',
            '/static/images/mars_orbiter.png',
            'Mars Orbit'
        ),
        (
            'DSCOVR',
            None,
            '2015-02-11', 'NASA / NOAA (USA)', 'Active',
            'DSCOVR (Deep Space Climate Observatory) orbits the Sun-Earth L1 point, providing real-time solar wind monitoring and stunning full-disk images of Earth\'s sunlit side. It acts as a sentinel for potentially dangerous solar storms.',
            '/static/images/hubble.png',
            'Sun-Earth L1 Lagrange Point'
        ),


        (
            'Parker Solar Probe',
            None,
            '2018-08-12', 'NASA (USA)', 'Active',
            'The Parker Solar Probe is the fastest human-made object ever, reaching speeds over 700,000 km/h. It flies through the Sun\'s corona, making groundbreaking discoveries about solar wind acceleration and the Sun\'s magnetic field structure.',
            '/static/images/parker_probe.png',
            'Heliocentric (Sun-grazing)'
        ),
        (
            'TESS',
            pid.get('Earth'),
            '2018-04-18', 'NASA (USA)', 'Active',
            'TESS (Transiting Exoplanet Survey Satellite) is Kepler\'s successor, surveying the entire sky for exoplanets around the nearest and brightest stars. It has already discovered thousands of planet candidates, including several in habitable zones.',
            '/static/images/hubble.png',
            'Highly Elliptical Orbit'
        ),
        (
            'Perseverance Rover',
            pid.get('Mars'),
            '2020-07-30', 'NASA (USA)', 'Active',
            'Perseverance is exploring Jezero Crater on Mars, searching for signs of ancient microbial life. It carries the Ingenuity helicopter (first powered flight on another planet) and is collecting rock samples for future return to Earth.',
            '/static/images/mars_orbiter.png',
            'Mars Surface'
        ),
        (
            'James Webb Space Telescope',
            pid.get('Earth'),
            '2021-12-25', 'NASA / ESA / CSA', 'Active',
            'JWST is the most powerful space telescope ever built. Operating primarily in infrared from the Sun-Earth L2 point, it peers back to the first galaxies formed after the Big Bang, studies exoplanet atmospheres, and reveals hidden details of stellar nurseries.',
            '/static/images/jwst.png',
            'Sun-Earth L2 Lagrange Point'
        ),
        (
            'DART',
            None,
            '2021-11-24', 'NASA (USA)', 'Completed',
            'DART (Double Asteroid Redirection Test) was humanity\'s first planetary defense mission. In September 2022, it deliberately crashed into asteroid Dimorphos, successfully altering its orbit — proving that we can deflect a potentially hazardous asteroid.',
            '/static/images/voyager.png',
            'Heliocentric (Asteroid Impact)'
        ),
        (
            'Chandrayaan-3',
            None,
            '2023-07-14', 'ISRO (India)', 'Completed',
            'Chandrayaan-3 made India the fourth country to land on the Moon and the first to land near the lunar south pole. Its Vikram lander and Pragyan rover studied the lunar surface composition and detected sulfur near the south pole.',
            '/static/images/lunar_orbiter.png',
            'Lunar Surface (South Pole)'
        ),
        (
            'Euclid',
            None,
            '2023-07-01', 'ESA', 'Active',
            'Euclid is a space telescope designed to explore the dark universe. By mapping billions of galaxies across 10 billion light-years, it aims to understand the nature of dark energy and dark matter that make up 95% of the cosmos.',
            '/static/images/jwst.png',
            'Sun-Earth L2 Lagrange Point'
        ),
        (
            'Aditya-L1',
            None,
            '2023-09-02', 'ISRO (India)', 'Active',
            'Aditya-L1 is India\'s first solar observation mission, positioned at the Sun-Earth L1 point. It continuously observes the Sun\'s corona, solar flares, and coronal mass ejections to improve our understanding of space weather and its effects on Earth.',
            '/static/images/parker_probe.png',
            'Sun-Earth L1 Lagrange Point'
        ),
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO satellites
        (name, planet_id, launch_date, agency, status, description, image_url, orbit_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', satellites)


def seed_news(cursor):
    news_articles = [
        (
            'James Webb Telescope Discovers New Exoplanet Atmosphere',
            'NASA\'s James Webb Space Telescope has made a groundbreaking discovery, identifying complex organic molecules in the atmosphere of exoplanet K2-18 b. The detection of dimethyl sulfide, a molecule only produced by life on Earth, has sparked excitement in the scientific community about the possibility of biological activity on this distant world.',
            'Discovery',
            'https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=600',
            'https://www.nasa.gov/mission/webb/',
            '2026-03-18 10:00:00'
        ),
        (
            'SpaceX Starship Completes First Orbital Refueling Test',
            'SpaceX has successfully demonstrated orbital propellant transfer between two Starship vehicles in Earth orbit. This milestone is critical for NASA\'s Artemis program, which plans to use Starship as the Human Landing System for returning astronauts to the Moon.',
            'Mission',
            'https://images.unsplash.com/photo-1541185933-ef5d8ed016c2?w=600',
            'https://www.spacex.com/vehicles/starship/',
            '2026-03-17 14:30:00'
        ),
        (
            'Mars Rover Perseverance Finds New Evidence of Ancient River',
            'NASA\'s Perseverance rover has discovered compelling evidence of an ancient river delta in Jezero Crater on Mars. The rover\'s samples contain layered sedimentary rocks with minerals that typically form in water, potentially containing fossilized signs of microbial life.',
            'Mars',
            'https://images.unsplash.com/photo-1614728263952-84ea256f9679?w=600',
            'https://mars.nasa.gov/mars2020/',
            '2026-03-16 09:15:00'
        ),
        (
            'New Record: 200th Spacewalk Conducted at ISS',
            'Astronauts aboard the International Space Station have completed the 200th spacewalk in the station\'s history. During the 6.5-hour excursion, the crew installed new solar array panels and upgraded external communication equipment.',
            'ISS',
            'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=600',
            'https://www.nasa.gov/international-space-station/',
            '2026-03-15 16:45:00'
        ),
        (
            'Saturn\'s Rings Are Disappearing Faster Than Expected',
            'New observations confirm that Saturn\'s iconic rings are eroding at a faster rate than previously estimated. Scientists predict the rings could vanish entirely within the next 100 million years, pulled in by Saturn\'s gravity as a dusty rain of ice particles.',
            'Saturn',
            'https://images.unsplash.com/photo-1614732414444-096e5f1122d5?w=600',
            'https://science.nasa.gov/saturn/',
            '2026-03-14 11:20:00'
        ),
        (
            'China Launches Ambitious Asteroid Mining Mission',
            'China\'s space agency has launched its first asteroid prospecting mission, targeting a near-Earth asteroid rich in platinum-group metals. The spacecraft will study composition and test extraction technologies for deep-space resource utilization.',
            'Mission',
            'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600',
            'https://www.space.com/',
            '2026-03-13 08:00:00'
        ),
        (
            'Jupiter\'s Moon Europa Confirmed to Have Subsurface Ocean',
            'Data from the Juno spacecraft has provided the strongest evidence yet that Europa has a global subsurface ocean beneath its icy crust. The ocean may contain twice as much water as Earth\'s oceans combined.',
            'Discovery',
            'https://images.unsplash.com/photo-1639921884918-8d28ab2e39a4?w=600',
            'https://europa.nasa.gov/',
            '2026-03-12 13:10:00'
        ),
        (
            'NASA Announces Artemis IV Crew for Lunar Gateway Assembly',
            'NASA has named the four astronauts who will crew the Artemis IV mission, the first to visit the Lunar Gateway space station. The mission is planned for 2028 and will include a 30-day stay in lunar orbit.',
            'Mission',
            'https://images.unsplash.com/photo-1522030299830-16b8d3d049fe?w=600',
            'https://www.nasa.gov/artemis/',
            '2026-03-11 15:30:00'
        ),
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO news (title, content, category, image_url, source_url, published_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', news_articles)


def seed_all():
    reset_db()
    conn = get_db()
    cursor = conn.cursor()

    seed_planets(cursor)
    seed_satellites(cursor)
    seed_news(cursor)

    conn.commit()

    p_count = cursor.execute('SELECT COUNT(*) FROM planets').fetchone()[0]
    s_count = cursor.execute('SELECT COUNT(*) FROM satellites').fetchone()[0]
    n_count = cursor.execute('SELECT COUNT(*) FROM news').fetchone()[0]

    conn.close()
    print("Database seeded successfully!")
    print(f"  - {p_count} planets")
    print(f"  - {s_count} satellites (Sputnik 1 to Aditya-L1)")
    print(f"  - {n_count} news articles")


if __name__ == '__main__':
    seed_all()
