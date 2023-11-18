from flask import Flask, render_template, request, session, redirect, url_for
import config
import	mysql.connector
import jsonify

app = Flask(__name__)
app.secret_key = "super secret key"

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
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    id_student = request.form['id_student']
    password = request.form['password']

    cur = mydb.cursor()
    cur.execute("SELECT * FROM Students WHERE idStudent = %s AND Password = %s", (id_student, password))
    user = cur.fetchone()
    print(user)
    cur.close()

    if user is not None:
        session['idStudent'] = id_student
        session['Name'] = user[2]
        session['LastName'] = user[4]
        session['Email'] = user[5]
        print('Bienvenido')
        return redirect(url_for('subjects'))
    else:
        return render_template('index.html', message="Las credenciales no son correctas")    

@app.route('/subjects', methods=['GET'])
def subjects():
    StudentID = session['idStudent']
    cur = mydb.cursor()
    cur.execute("SELECT S.idSubject, S.Name, S.idDept, X.NRC  FROM Subject as S join (SELECT C.idSubject as ID, C.NRC as NRC FROM Courses as C JOIN CoursesRegister as CR ON C.NRC = CR.NRC JOIN Students as E ON E.idStudent = CR.idStudent WHERE E.idStudent = %s) as X ON X.ID = S.idSubject", [StudentID])
    sub = cur.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cur.description]
    for record in sub:
        insertObject.append(dict(zip(columnNames, record)))
    cur.close()
    print(insertObject)
    return render_template('subjects.html', subjects = insertObject)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/subjects/<string:card_name>/<int:NRC>', methods=['GET', 'POST'])
def subject(card_name,NRC):
    StudentID = session['idStudent']
    print(StudentID)
    print(NRC)
    cur = mydb.cursor()
    cur.execute("SELECT * FROM Tasks WHERE idStudent  = %s and NRC = %s", (StudentID,NRC))
    tasks = cur.fetchall()

    insertObject = []
    columnNames = [column[0] for column in cur.description]
    for record in tasks:
        insertObject.append(dict(zip(columnNames, record)))
    cur.close()
    return render_template('course.html', tasks = insertObject)

if __name__ == '__main__':
        app.run(debug=True)