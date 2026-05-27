def mapearRelacoes(tabelas):
    relacoes = []

    for tabela in tabelas:
        for constraint in tabela["constraints"]:
            if constraint["tipo"] == "FK":
                relacoes.append({
                    "tabela_origem": tabela["nome"],
                    "coluna_origem": constraint["coluna"],
                    "tabela_destino": constraint["tabela_ref"],
                    "constraint": constraint["nome"]
                })

    return relacoes


def resumoRelacoes(relacoes):
    resumo = {}

    for rel in relacoes:
        origem = rel["tabela_origem"]

        if origem not in resumo:
            resumo[origem] = {
                "aponta_para": [],
                "recebe_de": []
            }

        destino = rel["tabela_destino"]
        if destino not in resumo:
            resumo[destino] = {
                "aponta_para": [],
                "recebe_de": []
            }

        resumo[origem]["aponta_para"].append(destino)
        resumo[destino]["recebe_de"].append(origem)

    return resumo