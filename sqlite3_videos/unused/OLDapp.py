import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('video.db')
    conn.row_factory = sqlite3.Row
    return conn

#maybe need later idk
# def get_post(post_id):
#     conn = get_db_connection()
#     post = conn.execute('SELECT * FROM posts WHERE id = ?',
#                         (post_id,)).fetchone()
#     conn.close()
#     if post is None:
#         abort(404)
#     return post


@app.route('/')
def start():
    return "Nothing here to see"

# @app.route('/search' , methods=['GET'])
# def search(input_title):
#     conn = get_db_connection()
#     videos = conn.execute('SELECT * FROM video WHERE title = ?', (input_title, ))
#     conn.close()
#     return render_template('search.html', videos=videos)

# ...

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


# https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
# 
# run
# set FLASK_APP=app
# set FLASK_ENV=development
# python -m flask run  << run flask >> instead of the linux command flask run