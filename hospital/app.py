from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore


app = Flask(__name__)



cred = credentials.Certificate("firebase-key.json")

firebase_admin.initialize_app(cred)

db = firestore.client()




@app.route("/")
def index():

    pacientes = db.collection("pacientes").stream()
    medicos = db.collection("medicos").stream()
    consultas = db.collection("consultas").stream()

    lista_pacientes = []

    for paciente in pacientes:

        dados = paciente.to_dict()

        dados["id"] = paciente.id

        lista_pacientes.append(dados)


    lista_medicos = []

    for medico in medicos:

        dados = medico.to_dict()

        dados["id"] = medico.id

        lista_medicos.append(dados)


    lista_consultas = []

    for consulta in consultas:

        dados = consulta.to_dict()

        dados["id"] = consulta.id

        
        paciente = db.collection("pacientes").document(
            dados["pacienteId"]
        ).get()

        if paciente.exists:
            dados["paciente"] = paciente.to_dict()["nome"]
        else:
            dados["paciente"] = "Não encontrado"


        
        medico = db.collection("medicos").document(
            dados["medicoId"]
        ).get()

        if medico.exists:
            dados["medico"] = medico.to_dict()["nome"]
        else:
            dados["medico"] = "Não encontrado"


        lista_consultas.append(dados)


    return render_template(
        "index.html",
        pacientes=lista_pacientes,
        medicos=lista_medicos,
        consultas=lista_consultas
    )



@app.route("/paciente/cadastrar", methods=["POST"])
def cadastrar_paciente():

    nome = request.form["nome"]
    idade = request.form["idade"]
    cpf = request.form["cpf"]


    db.collection("pacientes").add({
        "nome": nome,
        "idade": int(idade),
        "cpf": cpf
    })


    return redirect(url_for("index"))




@app.route("/paciente/excluir/<id>")
def excluir_paciente(id):

    db.collection("pacientes").document(id).delete()

    return redirect(url_for("index"))




@app.route("/paciente/editar/<id>", methods=["POST"])
def editar_paciente(id):

    nome = request.form["nome"]
    idade = request.form["idade"]
    cpf = request.form["cpf"]


    db.collection("pacientes").document(id).update({

        "nome": nome,
        "idade": int(idade),
        "cpf": cpf

    })


    return redirect(url_for("index"))



@app.route("/medico/cadastrar", methods=["POST"])
def cadastrar_medico():

    nome = request.form["nome"]
    especialidade = request.form["especialidade"]
    crm = request.form["crm"]


    db.collection("medicos").add({

        "nome": nome,
        "especialidade": especialidade,
        "crm": crm

    })


    return redirect(url_for("index"))




@app.route("/medico/excluir/<id>")
def excluir_medico(id):

    db.collection("medicos").document(id).delete()

    return redirect(url_for("index"))




@app.route("/medico/editar/<id>", methods=["POST"])
def editar_medico(id):

    nome = request.form["nome"]
    especialidade = request.form["especialidade"]
    crm = request.form["crm"]


    db.collection("medicos").document(id).update({

        "nome": nome,
        "especialidade": especialidade,
        "crm": crm

    })


    return redirect(url_for("index"))



@app.route("/consulta/cadastrar", methods=["POST"])
def cadastrar_consulta():

    paciente_id = request.form["pacienteId"]
    medico_id = request.form["medicoId"]
    data = request.form["data"]
    motivo = request.form["motivo"]


    db.collection("consultas").add({

        "pacienteId": paciente_id,
        "medicoId": medico_id,
        "data": data,
        "motivo": motivo

    })


    return redirect(url_for("index"))



@app.route("/consulta/excluir/<id>")
def excluir_consulta(id):

    db.collection("consultas").document(id).delete()

    return redirect(url_for("index"))



@app.route("/consulta/editar/<id>", methods=["POST"])
def editar_consulta(id):

    paciente_id = request.form["pacienteId"]
    medico_id = request.form["medicoId"]
    data = request.form["data"]
    motivo = request.form["motivo"]


    db.collection("consultas").document(id).update({

        "pacienteId": paciente_id,
        "medicoId": medico_id,
        "data": data,
        "motivo": motivo

    })


    return redirect(url_for("index"))


if __name__ == "__main__":

    app.run(debug=True)