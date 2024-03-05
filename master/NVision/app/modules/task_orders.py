import requests
import json

def update_task_status(task_id, status_value):
    url = f"http://localhost:3000/tasks/update"
    body = {
        'task_id':task_id,
        'status_value':status_value
    }
    json_body = json.dumps(body)
    headers = {'Content-Type':'application/json'}
    update_response = requests.post(url,data=json_body,headers=headers)
    print(update_response.json()[0]['update_model_task_status'])

async def create_model_entry(task_id,folder_name):
    url = f"http://localhost:3000/models/create"
    body = {
        'task_id':task_id,
        'location_name':folder_name
    }
    json_body = json.dumps(body)
    headers = {'Content-Type':'application/json'}
    try:
        creation_response = requests.post(url,data=json_body,headers=headers)
        print(creation_response.json()[0]['insert_models'])
        return True
    except:
        return False