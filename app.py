from flask import Flask, render_template, request, session
from flask_session import Session
from control_python.Usuario import Usuario, InvalidPassWordError, UserDoesNotExist
from control_python.controleUsuario import createUser, UserExist
from control_python.controleTarefa import addTask as adTa, updateTask as upTa
from control_python.controleProjeto import addProject as adPro
from control_python.controleTime import memberInTeam , addMember
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)


@app.route("/")
def render_login():
    return render_template('login.html', user=False, msg='')


@app.post('/register')
def register():
    name = request.form['name'].strip()
    lastname = request.form['lastname'].strip()
    email = request.form['email'].strip()
    password = request.form['password'].strip()

    try:
        if createUser(name, lastname, email, password):
            return render_template('registerUser.html', user=True, msg='Usuário cadastrado com sucesso')
        else:
            return render_template('registerUser.html', user=True, msg='Não foi possível cadastrar o usuário')
    except UserExist:
        return render_template('registerUser.html', user=True, msg='Usuário já existe')


@app.route('/registerUser')
def registerUser():
    return render_template('registerUser.html')


@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        email = request.form['email'].strip()
        senha = request.form['senha'].strip()

        try:
            user = Usuario(email, senha)
            session['email'] = user.email
            session['password'] = user.password
            session['username'] = user.name
            session['userlastname'] = user.lastname
            session['User'] = user
        except InvalidPassWordError:
            return render_template('login.html', user=True, msg='Senha incorreta')
        except UserDoesNotExist:
            return render_template('login.html', user=True, msg='Usuário não existe')

        return render_template('index.html',
                               teams=session['User'].get_projectsxteams() if len(session['User'].get_projectsxteams()) > 0 else False)
    else:
        return render_template('index.html',
                               teams=session['User'].get_projectsxteams() if len(session['User'].get_projectsxteams()) > 0 else False)


@app.route('/admControl')
def admControl():
    owner_teams = session['User'].get_ownerteams()

    return render_template('admControl.html',
                           owner_teams=owner_teams)


@app.route('/addProject', methods=['GET', 'POST'])
def addProject():
    name = request.form['name'].strip()
    emails = request.form.getlist('emails[]')
    team_id = request.form['id']

    adPro(name, emails, team_id,
          session['email'],
          session['username'],
          session['userlastname'])

    return admControl()


@app.route('/addTask', methods=['POST', 'GET'])
def addTask():
    name = request.form['name'].strip()
    email = request.form['email']
    project_id = request.form['id']

    new_task = {'name': name, 'assigned': email, 'status': False}
    adTa(project_id, new_task)
    return admControl()


@app.route('/tasksControl')
def tasksControl():
    teams = session['User'].get_projectsxteams()

    new_teams = []

    for team in teams:
        if team['projects']:
            new_projects = []
            for project in team['projects']:
                new_tasks = []
                if project['tasks']:
                    for task in project['tasks']:
                        if task['assigned'] == session['email']:
                            new_tasks.append(task)

                project['tasks'] = new_tasks
                new_projects.append(project)

            new_teams.append({
                'equipe_id': team['equipe_id'],
                'name': team['name'],
                'owner_email': team['owner_email'],
                'owner_name': team['owner_name'],
                'members': team['members'],
                'projects': new_projects
            })

    return render_template('tasksControl.html', teams=new_teams)


@app.route('/updateTask', methods=['GET', 'POST'])
def updateTask():
    task_name, project_id = request.form['concluir'].split(',')

    r = upTa(project_id, task_name, session['email'])

    return tasksControl()


@app.route('/updateTeam', methods=['GET', 'POST'])
def updateTeam():
    email = request.form['email'].strip()
    team_id = request.form['id']

    if not memberInTeam(team_id , email):
        addMember(team_id , email)
    return admControl()

@app.route('/deleteMember', methods=['GET' , 'POST'])
def deleteMember():
    email = request.form['excluir']
    e , i = email.split(",")
    return e + i

if __name__ == '__main__':
    app.run()