import zlib

def encode6bit(b):
    if b < 10:
        return chr(48 + b)
    b -= 10
    if b < 26:
        return chr(65 + b)
    b -= 26
    if b < 26:
        return chr(97 + b)
    b -= 26
    if b == 0:
        return '-'
    if b == 1:
        return '_'
    return '?'


def encode3bytes(b1, b2, b3):
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return encode6bit(c1) + encode6bit(c2) + encode6bit(c3) + encode6bit(c4)


def encodarPlantuml(codigo):
    data = zlib.compress(codigo.encode('utf-8'), 9)[2:-4]

    res = ""
    for i in range(0, len(data), 3):
        if i + 2 == len(data):
            res += encode3bytes(data[i], data[i+1], 0)[:3]
        elif i + 1 == len(data):
            res += encode3bytes(data[i], 0, 0)[:2]
        else:
            res += encode3bytes(data[i], data[i+1], data[i+2])
    return res


def gerarUrlDiagrama(codigo_puml):
    encoded = encodarPlantuml(codigo_puml)
    return f"https://www.plantuml.com/plantuml/svg/{encoded}"

def gerarCodigoPuml(tabela, todas_tabelas):
    mapa = {t['nome']: t for t in todas_tabelas}

    relacionadas = set()
    for c in tabela['constraints']:
        if c['tipo'] == 'FK' and c['tabela_ref']:
            relacionadas.add(c['tabela_ref'])

    for t in todas_tabelas:
        for c in t['constraints']:
            if c['tipo'] == 'FK' and c['tabela_ref'] == tabela['nome']:
                relacionadas.add(t['nome'])

    linhas = ["@startuml", "skinparam linetype ortho", ""]

    linhas.append(f"entity \"{tabela['nome']}\" {{")
    for col in tabela['colunas']:
        pk = any(c['coluna'] == col['nome'] and c['tipo'] == 'PK' for c in tabela['constraints'])
        fk = any(c['coluna'] == col['nome'] and c['tipo'] == 'FK' for c in tabela['constraints'])
        prefixo = "* " if pk else "# " if fk else "  "
        linhas.append(f"  {prefixo}{col['nome']} : {col['tipo']}")
    linhas.append("}")
    linhas.append("")

    for nome_rel in relacionadas:
        if nome_rel in mapa:
            t_rel = mapa[nome_rel]
            linhas.append(f"entity \"{t_rel['nome']}\" {{")
            for col in t_rel['colunas']:
                pk = any(c['coluna'] == col['nome'] and c['tipo'] == 'PK' for c in t_rel['constraints'])
                fk = any(c['coluna'] == col['nome'] and c['tipo'] == 'FK' for c in t_rel['constraints'])
                prefixo = "* " if pk else "# " if fk else "  "
                linhas.append(f"  {prefixo}{col['nome']} : {col['tipo']}")
            linhas.append("}")
            linhas.append("")

    for c in tabela['constraints']:
        if c['tipo'] == 'FK' and c['tabela_ref']:
            linhas.append(f"\"{tabela['nome']}\" }}o--|| \"{c['tabela_ref']}\"")

    for t in todas_tabelas:
        for c in t['constraints']:
            if c['tipo'] == 'FK' and c['tabela_ref'] == tabela['nome']:
                linhas.append(f"\"{t['nome']}\" }}o--|| \"{tabela['nome']}\"")

    linhas.append("")
    linhas.append("@enduml")

    return "\n".join(linhas)