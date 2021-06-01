"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email= email, password= password)

    db.session.add(user)
    db.session.commit()

    return user

def get_users():

    users = User.query.all()

    return users   


def get_user_by_id(user_id):
    
    user = User.query.get(user_id)

    return user      

def get_user_by_email(email):

    user = User.query.filter(User.email == email).first()
    
    return user 
    
def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""
    
    movie = Movie(title= title, overview= overview, release_date= release_date, poster_path= poster_path)
    
    db.session.add(movie)
    db.session.commit()

    return movie

def get_movies():

        movies = Movie.query.all()
        return movies


def get_movie_by_id(movie_id):
    
    movie = Movie.query.get(movie_id)
    return movie         


def create_rating(score, user, movie):
    """Create and return a new rating."""
    
    rating = Rating(score= score, user= user, movie= movie)
    
    db.session.add(rating)
    db.session.commit()

    return rating    

def password_match(email):

    user = User.query.filter(User.email == email).first()
    password = user.password

    return password

def get_user_id(email):
    
    user = User.query.filter(User.email == email).first()       
    user_id = user.user_id

    return user_id

if __name__ == '__main__':
    from server import app
    connect_to_db(app)