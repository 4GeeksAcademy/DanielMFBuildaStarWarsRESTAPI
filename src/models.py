from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

characters_in_films = db.Table('characters_in_films',
                               db.Column('film_id', db.Integer, db.ForeignKey(
                                   'films.uid'), primary_key=True),
                               db.Column('person_id', db.Integer, db.ForeignKey(
                                   'people.uid'), primary_key=True)
                               )

films_planets = db.Table('films_planets',
                         db.Column('film_id', db.Integer, db.ForeignKey(
                             'films.uid'), primary_key=True),
                         db.Column('planet_id', db.Integer, db.ForeignKey(
                             'planets.uid'), primary_key=True)
                         )

films_starships = db.Table('films_starships',
                           db.Column('film_id', db.Integer, db.ForeignKey(
                               'films.uid'), primary_key=True),
                           db.Column('starship_id', db.Integer, db.ForeignKey(
                               'starships.uid'), primary_key=True)
                           )

films_vehicles = db.Table('films_vehicles',
                          db.Column('film_id', db.Integer, db.ForeignKey(
                              'films.uid'), primary_key=True),
                          db.Column('vehicle_id', db.Integer, db.ForeignKey(
                              'vehicles.uid'), primary_key=True)
                          )

films_species = db.Table('films_species',
                         db.Column('film_id', db.Integer, db.ForeignKey(
                             'films.uid'), primary_key=True),
                         db.Column('species_id', db.Integer, db.ForeignKey(
                             'species.uid'), primary_key=True)
                         )

starship_pilots = db.Table('starship_pilots',
                           db.Column('starship_id', db.Integer, db.ForeignKey(
                               'starships.uid'), primary_key=True),
                           db.Column('person_id', db.Integer, db.ForeignKey(
                               'people.uid'), primary_key=True)
                           )

vehicle_pilots = db.Table('vehicle_pilots',
                          db.Column('vehicle_id', db.Integer, db.ForeignKey(
                              'vehicles.uid'), primary_key=True),
                          db.Column('person_id', db.Integer, db.ForeignKey(
                              'people.uid'), primary_key=True)
                          )

species_people = db.Table('species_people',
                          db.Column('species_id', db.Integer, db.ForeignKey(
                              'species.uid'), primary_key=True),
                          db.Column('person_id', db.Integer, db.ForeignKey(
                              'people.uid'), primary_key=True)
                          )


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    favorites = db.relationship('Favorite', back_populates='user')

    def __repr__(self):
        return 'Username:{}, Favorites:{}'.format(self.username, self.favorites)

    def serialize(self):
        return {
            "username": self.username,
            "id": self.id,
            "favorites": [favorite.serialize() for favorite in self.favorites],
            "email": self.email,
            "is_active": self.is_active,
        }


class Planet(db.Model):
    __tablename__ = 'planets'
    uid = db.Column(db.Integer, primary_key=True)
    diameter = db.Column(db.String)
    rotation_period = db.Column(db.String)
    population = db.Column(db.String)
    terrain = db.Column(db.String)
    name = db.Column(db.String)


    films = db.relationship(
        'Film', secondary=films_planets, back_populates='planets')
    favorites = db.relationship('Favorite', back_populates='planet')

    def __repr__(self):
        return '{}'.format(self.name)

    def serialize(self):
        return {
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "population": self.population,
            "terrain": self.terrain
        }


class Person(db.Model):
    __tablename__ = 'people'
    uid = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.String)
    mass = db.Column(db.String)
    hair_color = db.Column(db.String)
    skin_color = db.Column(db.String)
    birth_year = db.Column(db.String)
    gender = db.Column(db.String)
    name = db.Column(db.String)

  
    vehicles = db.relationship(
        'Vehicle', secondary=vehicle_pilots, back_populates='pilots')
    species = db.relationship(
        'Species', secondary=species_people, back_populates='characters')
    starships = db.relationship(
        'Starship', secondary=starship_pilots, back_populates='pilots')
    films = db.relationship(
        'Film', secondary=characters_in_films, back_populates='characters')
    favorites = db.relationship('Favorite', back_populates='person')

    def __repr__(self):
        return '{}'.format(self.name)

    def serialize(self):
        return {
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "birth_year": self.birth_year,
            "starship": [starship.name for starship in self.starships],
            "films": [film.title for film in self.films],
        }


class Film(db.Model):
    __tablename__ = 'films'
    uid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    episode_id = db.Column(db.Integer)
    director = db.Column(db.String)
    opening_crawl = db.Column(db.String)

  
    characters = db.relationship(
        'Person', secondary=characters_in_films, back_populates='films')
    planets = db.relationship(
        'Planet', secondary=films_planets, back_populates='films')
    starships = db.relationship(
        'Starship', secondary=films_starships, back_populates='films')
    vehicles = db.relationship(
        'Vehicle', secondary=films_vehicles, back_populates='films')
    species = db.relationship(
        'Species', secondary=films_species, back_populates='films')
    favorites = db.relationship('Favorite', back_populates='film')

    def __repr__(self):
        return '{}'.format(self.title)

    def serialize(self):
        return {
            "title": self.title,
        }


class Starship(db.Model):
    __tablename__ = 'starships'
    uid = db.Column(db.Integer, primary_key=True)
    films = db.relationship(
        'Film', secondary=films_starships, back_populates='starships')
    name = db.Column(db.String)
    model = db.Column(db.String)
    vehicle_class = db.Column(db.String)
    manufacturer = db.Column(db.String)
    cost_in_credits = db.Column(db.String)
    pilots = db.relationship(
        'Person', secondary=starship_pilots, back_populates='starships')
    favorites = db.relationship('Favorite', back_populates='starship')

    def __repr__(self):
        return '{}'.format(self.name)

    def serialize(self):
        return {
            "name": self.name,
        }


class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    uid = db.Column(db.Integer, primary_key=True, nullable=True)
    name = db.Column(db.String)
    model = db.Column(db.String)
    vehicle_class = db.Column(db.String)
    manufacturer = db.Column(db.String)
    cost_in_credits = db.Column(db.String)
    films = db.relationship(
        'Film', secondary=films_vehicles, back_populates='vehicles')
    pilots = db.relationship(
        'Person', secondary=vehicle_pilots, back_populates='vehicles')
    favorites = db.relationship('Favorite', back_populates='vehicle')

    def __repr__(self):
        return '{}'.format(self.name)

    def serialize(self):
        return {
            "name": self.name,
        }


class Species(db.Model):
    __tablename__ = 'species'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    classification = db.Column(db.String)
    designation = db.Column(db.String)
    average_height = db.Column(db.String)
    average_lifespan = db.Column(db.String)
    hair_colors = db.Column(db.String)

  
    films = db.relationship(
        'Film', secondary=films_species, back_populates='species')
   
    characters = db.relationship(
        'Person', secondary=species_people, back_populates='species')
    favorites = db.relationship('Favorite', back_populates='species')

    def __repr__(self):
        return '{}'.format(self.name)

    def serialize(self):
        return {
            "name": self.name,
        }


class Favorite(db.Model):
    __tablename__ = 'favorites'
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=True)
    film_id = db.Column(db.Integer, db.ForeignKey(
        'films.uid'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey(
        'planets.uid'), nullable=True)
    person_id = db.Column(db.Integer, db.ForeignKey(
        'people.uid'), nullable=True)
    starship_id = db.Column(db.Integer, db.ForeignKey(
        'starships.uid'), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey(
        'vehicles.uid'), nullable=True)
    specie_id = db.Column(db.Integer, db.ForeignKey(
        'species.uid'), nullable=True)
    user = db.relationship('User', back_populates='favorites')
    film = db.relationship('Film', back_populates='favorites')
    planet = db.relationship('Planet', back_populates='favorites')
    person = db.relationship('Person', back_populates='favorites')
    starship = db.relationship('Starship', back_populates='favorites')
    vehicle = db.relationship('Vehicle', back_populates='favorites')
    species = db.relationship('Species', back_populates='favorites')
    __table_args__ = (
        db.PrimaryKeyConstraint('user_id', 'film_id', 'planet_id',
                                'person_id', 'starship_id', 'vehicle_id', 'specie_id'),
    )

    def __repr__(self):
        return 'Planets: {}, Film: {}, People: {}'.format(self.planet_id, self.film_id, self.person_id)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "film_id": self.film_id,
            "planet_id": self.planet_id,
            "person_id": self.person_id,
            "starship_id": self.starship_id,
            "vehicle_id": self.vehicle_id,
            "specie_id": self.specie_id
        }