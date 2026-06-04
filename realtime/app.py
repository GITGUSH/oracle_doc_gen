from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
import oracledb

app = Flask(__name__)
app.secret_key = "oracle_doc_gen_secret"

CONNECTIONS_FILE = "connections.json"


def carregarConexoes():
    if not os.path.exists(CONNECTIONS_FILE):
        return {}
    with open(CONNECTIONS_FILE, "r") as f:
        return json.load(f)


def salvarConexoes(conexoes):
    with open(CONNECTIONS_FILE, "w") as f:
        json.dump(conexoes, f, indent=4)


def testarConexao(host, porta, service, usuario, senha):
    try:
        con = oracledb.connect(
            user=usuario,
            password=senha,
            dsn=f"{host}:{porta}/{service}"
        )
        con.close()
        return True
    except Exception as e:
        return str(e)


@app.route("/")
def index():
    conexoes = carregarConexoes()
    erro = request.args.get("erro")
    return render_template("index.html", conexoes=conexoes, erro=erro)


@app.route("/conectar", methods=["POST"])
def conectar():
    nome    = request.form.get("nome")
    host    = request.form.get("host")
    porta   = request.form.get("porta", 1521)
    service = request.form.get("service")
    usuario = request.form.get("usuario")
    senha   = request.form.get("senha")
    salvar  = request.form.get("salvar")

    resultado = testarConexao(host, int(porta), service, usuario, senha)

    if resultado is not True:
        return redirect(url_for("index", erro=resultado))

    session["host"]    = host
    session["porta"]   = int(porta)
    session["service"] = service
    session["usuario"] = usuario
    session["senha"]   = senha
    session["schema"]  = usuario.upper()
    session["nome"]    = nome or usuario.upper()

    if salvar and nome:
        conexoes = carregarConexoes()
        conexoes[nome] = {
            "host":    host,
            "porta":   int(porta),
            "service": service,
            "usuario": usuario,
            "senha":   senha
        }
        salvarConexoes(conexoes)

    return redirect(url_for("dashboard"))


@app.route("/usar/<nome>")
def usarConexao(nome):
    conexoes = carregarConexoes()
    if nome not in conexoes:
        return redirect(url_for("index"))

    c = conexoes[nome]
    resultado = testarConexao(c["host"], c["porta"], c["service"], c["usuario"], c["senha"])

    if resultado is not True:
        return redirect(url_for("index", erro=resultado))

    session["host"]    = c["host"]
    session["porta"]   = c["porta"]
    session["service"] = c["service"]
    session["usuario"] = c["usuario"]
    session["senha"]   = c["senha"]
    session["schema"]  = c["usuario"].upper()
    session["nome"]    = nome

    return redirect(url_for("dashboard"))


@app.route("/deletar/<nome>")
def deletarConexao(nome):
    conexoes = carregarConexoes()
    if nome in conexoes:
        del conexoes[nome]
        salvarConexoes(conexoes)
    return redirect(url_for("index"))


@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("index"))
    return render_template("dashboard.html", session=session)


@app.route("/desconectar")
def desconectar():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)