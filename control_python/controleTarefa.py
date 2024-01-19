from control_python.crud import conect, update, select
from bson import ObjectId


def addTask(project_id: str, task: dict) -> bool:
    try:
        client = conect()
        db = client['Projeto_4_Bimestre']

        new_id = ObjectId(project_id)

        project = select('projetos', db, {'_id': {'$eq': new_id}})[0]

        project['tasks'].append(task)

        r = update('projetos', db, {'_id': {'$eq': new_id}},
                   {'$set': {'tasks': project['tasks']}})

        client.close()
        return r
    except:
        return False


def updateTask(project_id: str, task_name: str, assigned: str) -> bool:
    
        client = conect()
        db = client['Projeto_4_Bimestre']

        new_id = ObjectId(project_id)

        project = select('projetos', db, {'_id': {'$eq': new_id}})[0]

        i = 0
        for task in project['tasks']:
            if (task['assigned'] == assigned) and (task['name'] == task_name) and (task['status'] == False):
                new_task = {'name': task['name'],
                            'assigned': task['assigned'],
                            'status': True}
                del project['tasks'][i]
                project['tasks'].append(new_task)
                break
            i+=1

        r = update('projetos', db, {'_id': {'$eq': new_id}},
                   {'$set': {'tasks': project['tasks']}})

        client.close()
        return r
