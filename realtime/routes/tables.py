from flask import Blueprint, render_template, redirect, url_for, session
from services.conexao_service import conectarBanco
from services.objeto_service import carregarTabelas

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

        objeto = carregarTabelas(cursor)

        tabelas = [
            {
                "nome": t["nome"],
                "registros": t.get("registros", "-"),
                "colunas": len(t["colunas"]),
                "status": t.get("status", "VALID")
            }
            for t in objeto
        ]

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()
    
    return render_template("tables.html", tabelas=tabelas, session=session)