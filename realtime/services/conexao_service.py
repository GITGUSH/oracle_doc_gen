from flask import session
import json
import os
import oracledb
from dotenv import load_dotenv

load_dotenv()
connections_file = os.getenv("CONNECTIONS_FILE")

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