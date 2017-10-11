# COMPLETE set up flask - import things, set up app, debug, app run, def index
# COMPLETE set up handlers and templates
# COMPLETE set up database, user
# COMPLETE set up SQLAlchemy
# COMPLETE set up Models
# COMPLETE submission separate from listings
# COMPLETE separate add a new post and blog listing into two routes, handler classes, templates
# COMPLETE user submits a new post, redirect them to the main blog page
# COMPLETE blog class with id, title, body
# COMPLETE /blog route displays blog posts
# COMPLETE submit new post at the /newpost route, display on main page
# COMPLETE two templates /blog and /newpost
# COMPLETE have a base to extend on blog and newpost
# COMPLETE in base template, have navigation links to the main blog page and new blog page
# COMPLETE validation - title and body of blog can't be blank, render to add a new post form, with error message
# TODO come back to Display Individual Entries later
# TODO do a CSS template later

from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'fjeioa;;fjeiaow;'

class Blog_Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140), nullable=False)
    body = db.Column(db.String(500), nullable=False)

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog')
def blog():
    blogs = Blog_Post.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route('/newpost', methods = ['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if not title or not body:
            flash("Please enter a title and body for each post.", 'error')
            return redirect('/newpost')
            #do i need these if it's nullable? how would I add flash message?
        else:
            newpost = Blog_Post(title, body)
            db.session.add(newpost)
            db.session.commit()
            return redirect('/blog')
    
    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()