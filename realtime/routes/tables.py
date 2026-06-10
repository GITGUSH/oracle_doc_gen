from flask import Blueprint, render_template, redirect, url_for, session
from services.conexao_service import conectarBanco
from services.objeto_service import carregarObjetos, gerarCodigoPuml, gerarUrlDiagrama

tables_bp = Blueprint("tables", __name__)

@tables_bp.route("/tables")
def tablesIndex():
    if "usuario" not in session:
        return redirect(url_for("auth.index"))
    
    con = None
    cursor = None

    try:
        con = conectarBanco()
        cursor = con.cursor()

        objetos = carregarObjetos(cursor)

        tabelas = []
        for t in objetos["tabelas"]:
            tabelas.append({
                "nome": t["nome"],
                "registros": t.get("registros", "-"),
                "colunas": len(t["colunas"]),
                "status": t.get("status", "VALID")
            })

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()
    
    return render_template("tables.html", tabelas=tabelas, session=session)