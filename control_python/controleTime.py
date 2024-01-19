from control_python.crud import conect, select , update
from control_python.controleUsuario import user_exist
from bson import ObjectId

def addMember(team_id: str , member_email: str) -> bool:
    try:
        client = conect()
        db = client['Projeto_4_Bimestre']

        if user_exist(member_email) and not memberInTeam(team_id , member_email):
            user = select('usuarios' , db , {'email': {'$eq': member_email}})[0]

            data = {'name': user['name'],
                    'lastname': user['lastname'],
                    'email': user['email']}

            new_id = ObjectId(team_id)
            team = select('equipes' , db , {'_id': {'$eq': new_id}})[0]
            
            team['members'].append(data)

            r = update('equipes' , db , {'_id': {'$eq': new_id}} , {'$set': {'members': team['members']}})
            return r
        else:
            return False
    except:
        return False


def memberInTeam(team_id: str , member_email: str) -> bool:
    client = conect()
    db = client['Projeto_4_Bimestre']
    
    new_id = ObjectId(team_id)

    team = select('equipes' , db , {'_id': {'$eq': new_id}})[0]
    client.close()
    for user in team['members']:
        if user['email'] == member_email:
            return True
    
    return False

