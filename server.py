from flask import Flask, render_template, request, session, redirect, url_for
import config
import	mysql.connector

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
def course(card_name,NRC):
    session['card_name'] = card_name
    session['NRC'] = NRC
    StudentID = session['idStudent']
    cur = mydb.cursor()
    
    #Profesor, departamento 
    cur.execute("SELECT DISTINCT P.Name, P.MiddleName, P.LastName, P.Email, D.NameDept FROM CoursesProf AS CP JOIN Professors AS P ON P.idProfessor = CP.idProfessor JOIN Departments AS D ON D.idDept = P.idDept JOIN CoursesRegister AS CR ON CR.NRC = CP.NRC WHERE CR.NRC = %s;",[NRC])
    info = cur.fetchall()
    
    info = {
    'Name' : card_name,
    'ProfName': [info[i][0] + (' ' + str(info[i][1]) if info[i][1] is not None else '') + ' ' + info[i][2] for i in range(len(info))],
    'ProfEmail': [info[i][3] for i in range(len(info))],
    'NameDept': info[0][4]
    }
    cur.close()

    #Encontar tareas
    cur = mydb.cursor()
    cur.execute("SELECT * FROM Tasks WHERE idStudent  = %s and NRC = %s", (StudentID,NRC))
    tasks = cur.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cur.description]
    for record in tasks:
        insertObject.append(dict(zip(columnNames, record)))
    cur.close()

    #Econtrar ubicaciones
    cur = mydb.cursor()
    cur.execute("SELECT DISTINCT L.Name, L.Latitude, L.Longitude FROM Location L JOIN Schedules S ON L.idLocation = S.idLocation WHERE S.NRC = %s", [NRC])
    location = cur.fetchall()
    locations = []
    columnNames = [column[0] for column in cur.description]
    for record in location:
        locations.append(dict(zip(columnNames, record)))
    cur.close()

    #Encontrar Horarios
    cur = mydb.cursor()
    cur.execute("SELECT S.*, L.Name FROM Schedules S JOIN Location L ON S.idLocation = L.idLocation WHERE S.NRC = %s", [NRC])
    schedule = cur.fetchall()
    schedules = []
    columnNames = [column[0] for column in cur.description]
    for record in schedule:
        schedules.append(dict(zip(columnNames, record)))
    cur.close()



    return render_template('course.html', tasks = insertObject, info = info, locations = locations, schedules = schedules)

@app.route('/new-task', methods=['POST'])
def newTask():
    title = request.form['title']
    description = request.form['description']
    dateTask = request.form['date']
    idStudent = session.get('idStudent')
    NRC = session.get('NRC')

    if title and description and dateTask:
        cur = mydb.cursor()
        sql = "INSERT INTO Tasks (idTask, Title, Description, EndDate, Status, NRC, idStudent) VALUES (NULL, %s, %s, %s, 0, %s, %s)"
        data = (title, description, dateTask, NRC, idStudent)
        cur.execute(sql, data)
        mydb.commit()
        cur.close()
    return redirect(url_for('course', card_name = session.get('card_name'), NRC = session.get('NRC'), _anchor='tab-tasks'))


@app.route("/delete-task", methods=["POST"])
def deleteTask():
    print('-Borrar')
    cur = mydb.cursor()
    id = request.form['idTask']
    print(id)
    cur.execute("UPDATE Tasks SET Status = 1 WHERE idTask = %s",[id])
    mydb.commit()
    
    cur.close()
    return redirect(url_for('course', card_name = session.get('card_name'), NRC = session.get('NRC'), _anchor='tab-tasks'))

if __name__ == '__main__':
        app.run(debug=True)