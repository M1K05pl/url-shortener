import random
import string

def get_redirects(cur):  #get all redirects from db and put them into table
    rows = []
    res = cur.execute('select * from urls')
    for row in res:
        rows.append(row)
    return rows

def insert_url(longURL, shortURL, cur, con):
    cur.execute('insert into urls values ("{}", "{}")'.format(longURL, shortURL))
    con.commit()

def generate_random_url(cur):
    generatedString = ''
    for i in range(6):
        generatedString = generatedString + random.choice(string.ascii_letters)
    if check_if_string_available(generatedString, cur):
       return generatedString
    else:
        generate_random_url()

def check_if_string_available(string, cur):
    res = cur.execute('select longUrl from urls where shortUrl = "{}"'.format(string))
    if res.fetchone() is None:
        return True
    else:
        return False
    
def check_database(cur):
    try:
        res = cur.execute('select name from sqlite_master')
        if (res.fetchone() is None):
            cur.execute('create table urls(longUrl, shortUrl)')
        print('Database is connected.')
    except:
        print('Database is not connected.')
