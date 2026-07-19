import json
import os
import secrets
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
BASE_DIR = os.path.dirname(__file__)
DATA_FOLDER = os.path.join(BASE_DIR, "data")
DATABASE = os.path.join(BASE_DIR, "database", "database.db")

def cargar_json(nombre):
    with open(os.path.join(DATA_FOLDER, nombre), encoding="utf-8") as archivo:
        return json.load(archivo)

def iniciar_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    conexion = sqlite3.connect(DATABASE)
    conexion.execute("CREATE TABLE IF NOT EXISTS resultados(id INTEGER PRIMARY KEY AUTOINCREMENT, puntos INTEGER, salud INTEGER, fecha TEXT)")
    conexion.commit()
    conexion.close()

def guardar_resultado(puntos, salud):
    conexion = sqlite3.connect(DATABASE)
    conexion.execute("INSERT INTO resultados (puntos, salud, fecha) VALUES (?, ?, ?)", (puntos, salud, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conexion.commit()
    conexion.close()

iniciar_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/before-after")
def before_after():
    return render_template("before_after.html")

def iniciar_juego():
    session["pregunta"] = 0
    session["puntos"] = 0
    session["vidas"] = 3
    session["salud"] = 100
    session["feedback"] = None

@app.route("/game", methods=["GET", "POST"])
def game():
    preguntas = cargar_json("questions.json")
    if "pregunta" not in session or session["pregunta"] >= len(preguntas):
        iniciar_juego()
    if request.method == "POST":
        respuesta = int(request.form["answer"])
        correcta = preguntas[session["pregunta"]]["correct"]
        if respuesta == correcta:
            session["puntos"] += 10
        else:
            session["vidas"] -= 1
            session["salud"] -= 20
        session["feedback"] = {"seleccionada": respuesta, "correcta": correcta}
        return redirect(url_for("game"))
    if request.args.get("siguiente"):
        session["pregunta"] += 1
        session["feedback"] = None
        if session["pregunta"] >= len(preguntas):
            guardar_resultado(session["puntos"], session["salud"])
            session["resultado"] = "gano"
            return redirect(url_for("result"))
    if session["vidas"] <= 0 or session["salud"] <= 0:
        guardar_resultado(session["puntos"], session["salud"])
        session["resultado"] = "perdio"
        return redirect(url_for("result"))
    pregunta = preguntas[session["pregunta"]]
    return render_template("game.html", pregunta=pregunta, numero=session["pregunta"] + 1, total=len(preguntas), puntos=session["puntos"], vidas=session["vidas"], salud=session["salud"], feedback=session.get("feedback"))

@app.route("/game/reset")
def game_reset():
    iniciar_juego()
    return redirect(url_for("game"))

def iniciar_quiz():
    session["quiz_index"] = 0
    session["quiz_score"] = 0
    session["quiz_feedback"] = None

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    preguntas = cargar_json("facts.json")
    if "quiz_index" not in session or session["quiz_index"] > len(preguntas):
        iniciar_quiz()
    if request.method == "POST":
        respuesta = int(request.form["answer"])
        correcta = preguntas[session["quiz_index"]]["correct"]
        if respuesta == correcta:
            session["quiz_score"] += 10
        session["quiz_feedback"] = {"seleccionada": respuesta, "correcta": correcta}
        return redirect(url_for("quiz"))
    if request.args.get("siguiente"):
        session["quiz_index"] += 1
        session["quiz_feedback"] = None
    terminado = session["quiz_index"] >= len(preguntas)
    pregunta = None if terminado else preguntas[session["quiz_index"]]
    return render_template("quiz.html", pregunta=pregunta, numero=session["quiz_index"] + 1, total=len(preguntas), puntos=session["quiz_score"], feedback=session.get("quiz_feedback"), terminado=terminado)

@app.route("/quiz/reset")
def quiz_reset():
    iniciar_quiz()
    return redirect(url_for("quiz"))

@app.route("/result")
def result():
    puntos = session.get("puntos", 0)
    salud = max(session.get("salud", 100), 0)
    if salud >= 80:
        estado = "Excelente"
    elif salud >= 50:
        estado = "Bueno"
    elif salud > 0:
        estado = "En riesgo"
    else:
        estado = "Crítico"
    preguntas = cargar_json("questions.json")
    return render_template("result.html", gano=session.get("resultado") == "gano", puntos=puntos, puntaje_maximo=len(preguntas) * 10, salud=salud, impacto=salud, estado_planeta=estado)

def respuesta_bot(texto):
    tips = cargar_json("tips.json")
    texto = texto.lower()
    for palabra, respuesta in tips.items():
        if palabra != "default" and palabra in texto:
            return respuesta
    return tips["default"]

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    if "chat" not in session:
        session["chat"] = [{"autor": "bot", "texto": "Hola 🌱 Soy el bot ambiental."}]
    if request.method == "POST":
        mensaje = request.form.get("message", "")
        if mensaje:
            session["chat"].append({"autor": "user", "texto": mensaje})
            session["chat"].append({"autor": "bot", "texto": respuesta_bot(mensaje)})
            session.modified = True
        return redirect(url_for("chatbot"))
    return render_template("chatbot.html", historial=session["chat"])

@app.route("/chatbot/reset")
def chatbot_reset():
    session.pop("chat", None)
    return redirect(url_for("chatbot"))

if __name__ == "__main__":
    app.run(debug=True)