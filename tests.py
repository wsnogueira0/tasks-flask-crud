import pytest
import requests

#    CRUD
BASE_URL = "http://127.0.0.1:5000"

tasks = []


def test_create_task():
    new_task_data = {
        "title": "Nova Tarefas",
        "description": "Descrição da nova tarefa"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    # Utilizando o método request, coloque o método que irá utilizar, a base url e o end point do método, o json="variavel que vai como valor"
    assert response.status_code == 200
    # Serve para validar se  resposta vai bater
    response_json = response.json()
    assert "message" in response_json
    assert "id" in response_json
    # Verificando se a message e id existe na resposta json do create task
    tasks.append(response_json['id'])


def test_get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    response_json = response.json()

    assert response.status_code == 200
    assert "tasks" in response_json
    assert "total_tasks" in response_json


def test_get_task():
    if tasks:
        task_id = tasks[0]
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert task_id == response_json['id']


def test_update_task():
    if tasks:
        task_id = tasks[0]
        payload = {
            "title": "Título atualizado",
            "description": "Nova descrição",
            "completed": False
        }
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json

        # Nova requisição a tarefa especifica
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["title"] == payload["title"]
        assert response_json["description"] == payload["description"]
        assert response_json["completed"] == payload["completed"]


def test_delete_task():
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200

        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 404
