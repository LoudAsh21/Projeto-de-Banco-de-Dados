from control_python.crud import conect, insert, select
from bson import ObjectId


def addProject(project_name: str, members: list, equipe_id: str, owner_email: str, owner_name: str, owner_lastname: str) -> bool:
    try:
        client = conect()
        db = client['Projeto_4_Bimestre']

        new_id = ObjectId(equipe_id)
        new_members = getMembers(members)

        owner_data = {'email': owner_email,
                      'name': owner_name, 'lastname': owner_lastname}

        new_members.append(owner_data)

        project = {
            'equipe_id': new_id,
            'project_name': project_name,
            'members': new_members,
            'tasks': []
        }

        r = insert('projetos', db, project)
        client.close()
        return r
    except:
        return False

def getMembers(members: list) -> list:
    try:
        client = conect()
        db = client['Projeto_4_Bimestre']

        new_members = []

        for member in members:
            new_member = select('usuarios', db, {'email': {'$eq': member}})[0]

            new_members.append({'name': new_member['name'],
                                'lastname': new_member['lastname'],
                                'email': new_member['email']})

        client.close()

        return new_members
    except:
        return False