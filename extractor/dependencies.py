def extrairDependencies(cursor):
    cursor.execute("""
        SELECT
            name,
            type,
            referenced_name,
            referenced_type,
            referenced_owner
        FROM user_dependencies
        ORDER BY name, referenced_name
    """)

    dependencias = []
    for row in cursor.fetchall():
        dependencias.append({
            "nome": row[0],
            "tipo": row[1],
            "ref_nome": row[2],
            "ref_tipo": row[3],
            "ref_owner": row[4]
        })

    return dependencias


def agruparDependencias(dependencias):
    grafo = {}

    for dep in dependencias:
        nome = dep["nome"]

        if nome not in grafo:
            grafo[nome] = {
                "tipo": dep["tipo"],
                "depende_de": []
            }

        grafo[nome]["depende_de"].append({
            "nome": dep["ref_nome"],
            "tipo": dep["ref_tipo"],
            "owner": dep["ref_owner"]
        })

    return grafo