from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/ecogpt")
def ecogpt():
    return render_template("ecogpt.html")

if __name__ == "__main__":
    app.run(debug=True)