from flask import Blueprint, render_template, request, redirect, url_for, session
from services.conexao_service import conectarBanco
from services.objeto_service import carregarObjetos

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("auth.index"))
    
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