from control_python.crud import conect, insert
import bcrypt


def createUser(name: str, lastname: str, email: str, password: str) -> bool:
    client = conect()
    db = client['Projeto_4_Bimestre']

    if user_exist(email):
        raise UserExist

    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

    data = {'name': name, 'lastname': lastname, 'email': email,
            'password': pw_hash.decode('utf-8')}

    result = insert('usuarios', db, data)
    client.close()
    return result

def user_exist(email: str):
    try:
        client = conect()
        db = client['Projeto_4_Bimestre']
        collection = db['usuarios']
        data = collection.count_documents({'email': {'$eq': email}})
        client.close()
        if data > 0:
            return True
        else:
            return False
    except:
        return False

class UserExist(Exception):
    def __init__(self, message="Email já cadastrado"):
        self.message = message
        super().__init__(self.message)
