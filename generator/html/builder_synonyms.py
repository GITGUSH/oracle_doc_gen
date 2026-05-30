from generator.html.builder import lerTemplate, renderizar, salvarArquivo, linkObjeto

def gerarListaSynonyms(schema_data):
    schema = schema_data["schema"]
    synonyms = schema_data["synonyms"]

    linhas = ""
    for s in synonyms:
        linhas += f"""
        <tr>
            <td><a href="{s['nome'].lower()}.html">{s['nome']}</a></td>
            <td>{s['owner_referenciado'] or '-'}</td>
            <td>{s['objeto_referenciado']}</td>
            <td>{s['db_link'] or '-'}</td>
        </tr>
        """

    conteudo = f"""
    <input type="text" class="search-box" placeholder="Buscar synonym..." onkeyup="filtrarTabela(this)">
    <table id="tabelaLista">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Owner</th>
                <th>Objeto Referenciado</th>
                <th>DB Link</th>
            </tr>
        </thead>
        <tbody>
            {linhas}
        </tbody>
    </table>
    """

    template = lerTemplate("base.html")
    html = renderizar(template, {
        "titulo": "Synonyms",
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/synonyms/index.html", html)
    print("synonyms/index.html gerado.")


def gerarPaginaSynonym(schema, synonym):
    conteudo = f"""
    <div class="card">
        <h3>Informações Gerais</h3>
        <table>
            <tbody>
                <tr><td><strong>Nome</strong></td><td>{synonym['nome']}</td></tr>
                <tr><td><strong>Owner Referenciado</strong></td><td>{synonym['owner_referenciado'] or '-'}</td></tr>
                <tr><td><strong>Objeto Referenciado</strong></td><td>{synonym['objeto_referenciado']}</td></tr>
                <tr><td><strong>DB Link</strong></td><td>{synonym['db_link'] or '-'}</td></tr>
            </tbody>
        </table>
    </div>
    """

    template = lerTemplate("base.html")
    html = renderizar(template, {
        "titulo": synonym['nome'],
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/synonyms/{synonym['nome'].lower()}.html", html)


def gerarSynonyms(schema_data):
    schema = schema_data["schema"]
    gerarListaSynonyms(schema_data)

    for synonym in schema_data["synonyms"]:
        gerarPaginaSynonym(schema, synonym)

    print(f"{len(schema_data['synonyms'])} páginas de synonyms geradas.")