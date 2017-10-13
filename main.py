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

    if request.args:
        blog_id = request.args.get('id')
        post = Blog_Post.query.get(blog_id)
        return render_template('post.html', post=post)
   
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

@app.route('/')
def go_to_main():
    return redirect('/blog')

if __name__ == '__main__':
    app.run()