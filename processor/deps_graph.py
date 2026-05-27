def montarGrafoDeps(schema):
    grafo = {}

    objetos = [
        ("procedures", "PROCEDURE"),
        ("functions", "FUNCTION"),
        ("triggers", "TRIGGER"),
        ("views", "VIEW"),
    ]

    for chave, tipo in objetos:
        for obj in schema[chave]:
            nome = obj["nome"]

            if nome not in grafo:
                grafo[nome] = {
                    "tipo": tipo,
                    "depende_de": [],
                    "usado_por": []
                }

            for dep in obj["dependencias"]:
                grafo[nome]["depende_de"].append({
                    "nome": dep["nome"],
                    "tipo": dep["tipo"]
                })

    # monta o lado inverso — quem usa quem
    for nome, info in grafo.items():
        for dep in info["depende_de"]:
            dep_nome = dep["nome"]
            if dep_nome in grafo:
                grafo[dep_nome]["usado_por"].append({
                    "nome": nome,
                    "tipo": info["tipo"]
                })

    return grafo


def resumoGrafo(grafo):
    print(f"Total de objetos no grafo: {len(grafo)}\n")
    for nome, info in grafo.items():
        print(f"  → {nome} ({info['tipo']})")
        for dep in info["depende_de"]:
            print(f"    depende de: {dep['nome']} ({dep['tipo']})")
        for uso in info["usado_por"]:
            print(f"    usado por:  {uso['nome']} ({uso['tipo']})")
        print()