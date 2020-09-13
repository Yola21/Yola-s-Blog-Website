from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    author = db.Column(db.String(20), nullable=False, default='Anonymous')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return 'Blog Post ' + str(self.id)
    
#Flask uses this app.route for defining our url's
#Right now it has base url, i.e ('/')
@app.route('/') 

#For running on this url we are creating one function.
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET', 'POST'])
def posts():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('posts.html', posts = all_posts)

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

#If you want to pass any variable in the url you can do that by just defining function.
#It helps u in dynamic url's
@app.route('/home/<string:name>')
def hi(name):
    return "Hello, " + name + "!"

"""
U can also add multiple variable if u want in the url.
@app.route('/home/users/<string:name>/posts/<int:id>')
def hi(name, id):
    return "Hello, " + name + "!" + "your id is: " + id

"""
"""
Whichever function we write after route linearly, that function will be executed for that particular route.
@app.route('/home')
def hi():
    return "Hi There!!!"
"""

if __name__ == "__main__":
    app.run(debug=True)