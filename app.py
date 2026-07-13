from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

# CRUD
# Create, Read, Update and Delete

tasks = []
task_id_control = 1
# Observe qual a rota desejada e metódo que irá utilizar para criar a rota


@app.route("/tasks", methods=["POST"])
def create_task():
    # O comando de "global" permite que a var task_id_control criada seja usada dentro dessa função.
    # Isso tem que ser utilizada por ela ter sido criado fora do método e estou tentando acessar ela no método.
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data.get(
        "title", ""), description=data.get("description", ""))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "Nova tarefa criada com sucesso!"})


@app.route("/tasks", methods=["GET"])
def get_tasks():
    # o for em uma linha, está rodando a var task na lista tasks e transformando em dict pelo método importado to.dict(), e adicionando
    # automaticamente na lista task_list
    task_list = [task.to_dict() for task in tasks]

    output = {
        "tasks": task_list,
        "total_tasks": len(task_list)
    }

    return jsonify(output)

# Parâmetro de rota, o mesmo parâmetro utilizado deve ser recebedio na função criada nesse acesso de rota
# O valor do parâmetro sempre vem como STR deve ser convertido caso deseje outro type, como utilizado abaixo.


@app.route("/tasks/<int:id>", methods=["GET"])
def get_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())

    return jsonify({"message": "Não foi possível encontrar a atividade"}), 404


@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    if task == None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

    data = request.get_json()
    task.title = data["title"]
    task.description = data["description"]
    task.completed = data["completed"]

    return jsonify({"message": "Tarefa atualizada com sucesso"})


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    # Se o task for None
    if not task:
        return jsonify({"message": "Não foi possível encontrar a atividade."}), 404

    tasks.remove(task)
    return jsonify({"message": "Tarefa deletada com sucesso"})


if __name__ == "__main__":
    app.run(debug=True)
