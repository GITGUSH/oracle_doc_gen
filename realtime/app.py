from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
import oracledb
from dotenv import load_dotenv
import sys
import os
from extractor.tables import extrairTabelas
from extractor.views import extrairViews
from extractor.procedures import extrairProcedures
from extractor.functions import extrairFunctions
from extractor.packages import extrairPackages
from extractor.triggers import extrairTriggers
from extractor.sequences import extrairSequences
from extractor.indexes import extrairIndexes
from extractor.synonyms import extrairSynonyms
from extractor.jobs import extrairJobs

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
connections_file = os.getenv("CONNECTIONS_FILE")

if not app.secret_key:
    raise RuntimeError("SECRET_KEY não configurada")

if not connections_file:
    raise RuntimeError("CONNECTIONS_FILE não configurado")

def carregarConexoes():
    if not os.path.exists(connections_file):
        return {}
    with open(connections_file, "r", encoding="utf-8") as f:
        return json.load(f)


def salvarConexoes(conexoes):
    with open(connections_file, "w", encoding="utf-8") as f:
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
    
def conectarBanco():
    return oracledb.connect(
        user=session["usuario"],
        password=session["senha"],
        dsn=f"{session['host']}:{session['porta']}/{session['service']}"
    )

def carregarObjetos(cursor):
    return {
        "tabelas": extrairTabelas(cursor),
        "views": extrairViews(cursor),
        "procedures": extrairProcedures(cursor),
        "functions": extrairFunctions(cursor),
        "packages": extrairPackages(cursor),
        "triggers": extrairTriggers(cursor),
        "sequences": extrairSequences(cursor),
        "indexes": extrairIndexes(cursor),
        "synonyms": extrairSynonyms(cursor),
        "jobs": extrairJobs(cursor),
    }


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
    
    con = None
    cursor = None

    try:
        con = conectarBanco()
        cursor = con.cursor()

        objetos = carregarObjetos(cursor)

        resumo = {
            "tabelas":    len(objetos["tabelas"]),
            "views":      len(objetos["views"]),
            "procedures": len(objetos["procedures"]),
            "functions":  len(objetos["functions"]),
            "packages":   len(objetos["packages"]),
            "triggers":   len(objetos["triggers"]),
            "sequences":  len(objetos["sequences"]),
            "indexes":    len(objetos["indexes"]),
            "synonyms":   len(objetos["synonyms"]),
            "jobs":       len(objetos["jobs"]),
        }

        invalidos = []

        for v in objetos["views"]:
            if v.get("status", "VALID") != "VALID":
                invalidos.append({"nome": v["nome"], "tipo": "View"})

        for p in objetos["procedures"]:
            if p["status"] != "VALID":
                invalidos.append({"nome": p["nome"], "tipo": "Procedure"})

        for f in objetos["functions"]:
            if f["status"] != "VALID":
                invalidos.append({"nome": f["nome"], "tipo": "Function"})

        for p in objetos["packages"]:
            if p["status"] != "VALID":
                invalidos.append({"nome": p["nome"], "tipo": "Package"})

        for t in objetos["triggers"]:
            if t["status"] != "ENABLED":
                invalidos.append({"nome": t["nome"], "tipo": "Trigger"})
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()

    return render_template("dashboard.html", session=session, resumo=resumo, invalidos=invalidos)

@app.route("/desconectar")
def desconectar():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )