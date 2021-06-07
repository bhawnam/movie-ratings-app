"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/movies')
def all_movies():
    """View all movies."""

    movies = crud.get_movies()
    
    return render_template('all_movies.html', movies = movies)


@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """Show details on a particular movie."""

    movie = crud.get_movie_by_id(movie_id)
    
    return render_template('movie_details.html', movie = movie)


@app.route('/users')
def all_users():
    """View all users."""

    users = crud.get_users()
    
    return render_template('all_users.html', users = users)


@app.route('/users/<user_id>')
def show_user(user_id):

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user = user)


@app.route('/users', methods = ["POST"])
def register_user():
    
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    
    if user: 
        flash('Cannot create an account with that email. Try again.')
    else:
        crud.create_user(email, password) 
        flash('Account created - You can now log in!')

    return redirect('/')


@app.route('/login', methods = ["POST"])
def process_login():

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user.password == password:
        
        session['user'] = user.email
        flash(f'You have succesffully logged in {user.email}')
        return redirect('/movies')

    else: 
        flash('The email or password you entered was incorrect.') 
        return redirect('/')     


@app.route('/movies/<movie_id>/ratings', methods=['POST'])
def process_rating(movie_id):

    logged_in_email = session.get('user')
    rating = request.form.get('rating')

    if logged_in_email is None:
        flash("You must log in to rate a movie.")

    elif not rating:
        flash('You have not yet rated the movie.')

    else:
        user = crud.get_user_by_email(logged_in_email)
        movie = crud.get_movie_by_id(movie_id)    
    

        crud.create_rating(int(rating), user, movie)
        flash(f'You rated the movie {rating} out of 5')

    return redirect(f'/movies/{movie_id}')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
