from control_python.crud import conect, select
from control_python.controleUsuario import user_exist
import bcrypt



class Usuario:
    def __init__(self, email: str, password: str) -> None:
        client = conect()
        database = client['Projeto_4_Bimestre']
        if user_exist(email):
            self.email = email
            self.password = password
            data = select('usuarios', database, {'email': {'$eq': self.email}})
            self.name = data[0]['name']
            self.lastname = data[0]['lastname']
            client.close()
        else:
            raise UserDoesNotExist

    @property
    def password(self) -> hash:
        return self._password

    @password.setter
    def password(self, password: str):
        client = conect()
        db = client['Projeto_4_Bimestre']
        data = select('usuarios', db, {'email': {'$eq': self.email}})
        pw_hash = data[0]['password']
        test = bcrypt.checkpw(password.encode(
            'utf-8'), pw_hash.encode('utf-8'))

        if test:
            self._password = pw_hash
        else:
            raise InvalidPassWordError

    def get_projects(self):
        client = conect()
        db = client['Projeto_4_Bimestre']

        projects = select('projetos', db, {'members': {
            '$elemMatch': {'email': self.email}}})

        new_projects = []

        for project in projects:

            new_projects.append({'_id': project['_id'],
                                 'equipe_id': project['equipe_id'],
                                 'project_name': project['project_name'],
                                 'members': project['members'],
                                 'tasks': project['tasks'] if len(project['tasks']) > 0 else False})

        return new_projects

    def get_teams(self):
        client = conect()
        db = client['Projeto_4_Bimestre']

        teams = select('equipes', db, {'members': {
            '$elemMatch': {'email': self.email}}})

        new_teams = []
        for team in teams:
            new_teams.append(team)

        return new_teams

    def get_projectsxteams(self):
        teams = self.get_teams()
        projects = self.get_projects()

        projxteam = []
        for team in teams:
            new_projects = []
            for project in projects:
                if team['_id'] == project['equipe_id']:
                    new_projects.append(project)

            projxteam.append({'equipe_id': team['_id'],
                              'name': team['name'],
                              'owner_email': team['owner_email'],
                              'owner_name': team['owner_name'],
                              'members': team['members'],
                              'projects': new_projects if len(new_projects) > 0 else False})

        return projxteam

    def get_ownerteams(self):
        projteams = self.get_projectsxteams()

        owte = []

        for team in projteams:
            if team['owner_email'] == self.email:
                owte.append({
                    'equipe_id': team['equipe_id'],
                    'name': team['name'],
                    'owner_email': team['owner_email'],
                    'owner_name': team['owner_name'],
                    'members': team['members'],
                    'projects': team['projects']
                })

        return owte


class InvalidPassWordError(Exception):
    def __init__(self, message="Senha inválida"):
        self.message = message
        super().__init__(self.message)


class UserDoesNotExist(Exception):
    def __init__(self, message="Usuário não existe"):
        self.message = message
        super().__init__(self.message)
