import sqlite3
import os
from flask import Flask, redirect, render_template, request

from functions import get_redirects, insert_url, generate_random_url, check_database

app = Flask(__name__)

con = sqlite3.connect('urls.db', check_same_thread=False)
cur = con.cursor()

redirects = []


@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == "POST":
        original_url = request.form.get('longUrl')
        short_url = request.form.get('shortUrl')  
        if short_url is '':
            short_url = generate_random_url(cur)
            insert_url(original_url, short_url, cur, con)
        else:
            insert_url(original_url, short_url, cur, con) 
        global redirects 
        redirects = get_redirects(cur)
        return render_template('successful.html', original_url=original_url, short_url=short_url)
    else:
        return render_template('start.html')

@app.route('/<string:short_url>')
def short_url_redirect(short_url):
    global redirects
    for entry in redirects:
        if str(short_url) == str(entry[1]):
            return redirect(entry[0])
    return redirect('/')

@app.route('/cleardb')
def clear_db():
    cur.execute('delete from urls')
    con.commit()
    return 'Succesfully cleared the database.'

if __name__ == '__main__':
    check_database(cur)
    redirects = get_redirects(cur)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)