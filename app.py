import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import sqlalchemy
import pymysql
import pandas as pd


from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from os import environ

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')

   env_string = ''
   for name, value in os.environ.items():
       env_string += "{0}: {1}".format(name, value) + "\n"

   return render_template('index.html', numberdb = env_string)

@app.route('/db')

def db_test():
    print('Request for db page received')

    conn_str = os.environ.get('MYSQLCONNSTR_NumberDB')

    engine = sqlalchemy.create_engine(conn_str, pool_recycle=3600)
    #conn = engine.connect()

    df = pd.read_sql('SELECT * FROM NumberManagement.five9Account;', conn_str)

    table = df.to_html(index=False)

    return render_template('table.html', table=table)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
