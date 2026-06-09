from flask import Blueprint, render_template, request, redirect, url_for, session
from services.conexao_service import carregarConexoes, salvarConexoes, testarConexao

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def index():
    conexoes = carregarConexoes()
    erro = request.args.get("erro")
    return render_template("index.html", conexoes=conexoes, erro=erro)


@auth_bp.route("/conectar", methods=["POST"])
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
        return redirect(url_for("auth.index", erro=resultado))

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

    return redirect(url_for("dashboard.dashboard"))


@auth_bp.route("/usar/<nome>")
def usarConexao(nome):
    conexoes = carregarConexoes()
    if nome not in conexoes:
        return redirect(url_for("auth.index"))

    c = conexoes[nome]
    resultado = testarConexao(c["host"], c["porta"], c["service"], c["usuario"], c["senha"])

    if resultado is not True:
        return redirect(url_for("auth.index", erro=resultado))

    session["host"]    = c["host"]
    session["porta"]   = c["porta"]
    session["service"] = c["service"]
    session["usuario"] = c["usuario"]
    session["senha"]   = c["senha"]
    session["schema"]  = c["usuario"].upper()
    session["nome"]    = nome

    return redirect(url_for("dashboard.dashboard"))


@auth_bp.route("/deletar/<nome>")
def deletarConexao(nome):
    conexoes = carregarConexoes()
    if nome in conexoes:
        del conexoes[nome]
        salvarConexoes(conexoes)
    return redirect(url_for("auth.index"))

@auth_bp.route("/desconectar")
def desconectar():
    session.clear()
    return redirect(url_for("auth.index"))