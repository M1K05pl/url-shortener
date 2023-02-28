import sqlite3
import random
import string
import sys
import os
from flask import Flask, redirect, render_template, request


app = Flask(__name__)

con = sqlite3.connect('urls.db', check_same_thread=False)
cur = con.cursor()


redirects = []

def check_if_string_available(string):
    # try:
        res = cur.execute('select longUrl from urls where shortUrl = "{}"'.format(string))
        if res.fetchone() is None:
            return True
        else:
            return False
    # except:
    #     return True


def check_database():
    try:
        res = cur.execute('select name from sqlite_master')
        if (res.fetchone() is None):
            cur.execute('create table urls(longUrl, shortUrl)')
        print('Database is connected.')
    except:
        print('Database is not connected.')

def generate_random_url():
    generatedString = ''
    for i in range(6):
        generatedString = generatedString + random.choice(string.ascii_letters)
    if check_if_string_available(generatedString):
       return generatedString
    else:
        generate_random_url()


def insert_url(longURL, shortURL):
    cur.execute('insert into urls values ("{}", "{}")'.format(longURL, shortURL))
    con.commit()
    get_redirects()


def get_redirects():
    rows = []
    res = cur.execute('select * from urls')
    for row in res:
        rows.append(row)
    global redirects
    redirects = rows

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == "POST":
        original_url = request.form.get('longUrl')
        short_url = request.form.get('shortUrl')  
        if short_url is '':
            short_url = generate_random_url()
            insert_url(original_url, short_url)
        else:
            insert_url(original_url, short_url)   
        return render_template('successful.html', original_url=original_url, short_url=short_url)
    else:
        return render_template('start.html')

@app.route('/<string:short_url>')
def short_url_redirect(short_url):
    global redirects
    for entry in redirects:
        print(entry)
        if str(short_url) == str(entry[1]):
            return redirect(entry[0])
    return redirect('/')

@app.route('/cleardb')
def clear_db():
    cur.execute('delete from urls')
    con.commit()
    return 'Succesfully cleared the database.'

if __name__ == '__main__':
    check_database()
    get_redirects()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)