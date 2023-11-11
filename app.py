from flask import Flask, render_template, request, session, redirect, url_for
import config
import	mysql.connector

app = Flask(__name__)


#Connect to Database
try:
    mydb = mysql.connector.connect(
    host=config.MYSQL_ADDON_HOST,
    user=config.MYSQL_ADDON_USER,
    password=config.MYSQL_ADDON_PASSWORD,
    database=config.MYSQL_ADDON_DB
    )
    print('Succesfull')
except Exception as e:
    print(e)


#Pagina principal - Login
@app.route('/')
def index():
    return render_template('index.html')
    


if __name__ == '__main__':
        app.run(debug=True)