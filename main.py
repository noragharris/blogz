from flask import request, redirect, render_template, flash, session
import cgi

from app import app, db
from models import Blog_Post, User

app.secret_key = 'fjeioa;;fjeiaow;'

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verified_password = request.form['verify']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists, please visit login page.', 'error')
        elif not username or not password or not verified_password:
            flash('Please enter new username, password, and verified password.', 'error')
        elif password != verified_password:
            flash('Password and Verified Password do not match.', 'error')
        elif len(username) < 3 or len(username) > 15:
            flash('Username must be between 3 and 15 characters.', 'error')
        elif len(password) < 3 or len(password) > 20:
            flash('Password must be between 3 and 20 charachters.', 'error')
        else:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')    
    
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash('Logged in!')
            return redirect('/newpost')
        elif user and user.password != password:
            flash('Password incorrect.', 'error')
        else:
            flash('Username not recognized. Please go to signup page.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/')
def index():    
    if request.args.get('user'):
        user_username = request.args.get('user')
        user = User.query.filter_by(username = user_username).first()
        user_id = user.id
        blogs = Blog_Post.query.filter_by(owner_id = user_id).all()
        return render_template('singleUser.html', blogs=blogs)
    if request.args.get('blogid'):
        blog_id = request.args.get('blogid')
        post = Blog_Post.query.get(blog_id)
        return render_template('post.html', post = post)
    
    authors = User.query.all()
    return render_template('index.html', authors=authors)

@app.route('/blog')
def blog():
    if request.args:
        blog_id = request.args.get('blogid')
        post = Blog_Post.query.get(blog_id)
        return render_template('post.html', post=post)
   
    blogs = Blog_Post.query.all()
    return render_template('blog.html', blogs=blogs)
    

@app.route('/newpost', methods = ['POST', 'GET'])
def newpost():
    user = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        owner = user
        if not title or not body:
            flash("Please enter a title and body for each post.", 'error')
            return redirect('/newpost')
            # TODO do i need these if it's nullable? how would I add flash message?
        else:
            newpost = Blog_Post(title, body, owner, pub_date=None)
            db.session.add(newpost)
            db.session.commit()
            post = Blog_Post.query.get(newpost.id)
            return render_template('post.html', post=post)
            # TODO review if this is the best way to add a new post and display or if I should create a URL
    
    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()