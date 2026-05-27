import os
import shutil

def criarPastas(schema):
    pastas = [
        f"output/assets",
        f"output/{schema}/tables",
        f"output/{schema}/views",
        f"output/{schema}/procedures",
        f"output/{schema}/functions",
        f"output/{schema}/packages",
        f"output/{schema}/triggers",
        f"output/{schema}/sequences",
        f"output/{schema}/indexes",
        f"output/{schema}/synonyms",
        f"output/{schema}/jobs",
        f"output/{schema}/diagrams",
    ]

    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)

    print("Pastas criadas.")


def copiarAssets():
    origem = "generator/html/assets"
    destino = "output/assets"

    for arquivo in os.listdir(origem):
        shutil.copy(
            os.path.join(origem, arquivo),
            os.path.join(destino, arquivo)
        )

    print("Assets copiados.")


def lerTemplate(nome):
    caminho = f"generator/html/templates/{nome}"
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()


def renderizar(template, variaveis):
    for chave, valor in variaveis.items():
        template = template.replace("{{ " + chave + " }}", str(valor))
    return template


def salvarArquivo(caminho, conteudo):
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)