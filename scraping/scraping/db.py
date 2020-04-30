from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

# engine = None
Base = declarative_base()

class Film(Base):
    __tablename__ = 'films'
    
    id = Column(String, primary_key=True)
    title = Column(Text)

    reviews = relationship("Review", back_populates="film") # this attribute gets populated with the Review objects linked to this film

    def __str__(self):
        return "film : {}".format(self.title)

    def __repr__(self):
        return "<Film(id={}, title={})>".format(self.id, self.title)

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    film_id = Column(String, ForeignKey('films.id')) # code of the film
    user = Column(String(50), unique=True)
    rating = Column(String(5))
    date = Column(Date)
    review = Column(Text)

    film = relationship("Film", back_populates="reviews") # this attribute gets populated with the Film object linked to this review

    def __str__(self):
        return "user : {}\nreview : {}".format(self.user, self.review)

    def __repr__(self):
        return "<Review(id={}, film={}, user={}, date={}, rating={}, review={})>".format(self.id, self.film_id, self.user, self.date, self.rating, self.review)

# Base.metadata.create_all(engine)

class DBManager:
    """ Singleton class which is used to get only one database manager instance all over the project. """
    __instance = None
    engine = None

    def __init__(self):
        if DBManager.__instance == None:
            DBManager.__instance = self
            self.engine = create_engine('sqlite:///prova.db', echo=True)
            Base.metadata.create_all(self.engine)
        else:
            pass
    
    @staticmethod
    def getInstance():
        """ Static access method for always getting the reference to the only manager istance."""
        if DBManager.__instance == None:
            DBManager()
        return DBManager.__instance

    def addFilm(self, id, title):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        film = Film(id=id, title=title)
        session.add(film)

        session.commit()
        session.close()

    def addReview(self, user, rating, date, review, film):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        review_obj = Review(user=user, rating=rating, date=date, review=review, film=film)
        session.add(review_obj)

        session.commit()
        session.close()

    def getReviewsOf(self, filmID):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        film = session.query(Film).filter_by(id=filmID)
        session.close()
        return film.reviews

    def getFilmBy(self, ID):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        film = session.query(Film).filter_by(id=ID)
        session.close()
        return film