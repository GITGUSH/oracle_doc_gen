from generator.html.builder import lerTemplate, renderizar, salvarArquivo

def gerarListaIndexes(schema_data):
    schema = schema_data["schema"]
    indexes = schema_data["indexes"]

    # agrupa indexes por tabela
    tabelas = {}
    for i in indexes:
        tabela = i['tabela']
        if tabela not in tabelas:
            tabelas[tabela] = []
        tabelas[tabela].append(i)

    linhas = ""
    for tabela, idxs in sorted(tabelas.items()):
        linhas += f"""
        <tr>
            <td><a href="{tabela.lower()}.html">{tabela}</a></td>
            <td>{len(idxs)}</td>
        </tr>
        """

    conteudo = f"""
    <input type="text" class="search-box" placeholder="Buscar tabela..." onkeyup="filtrarTabela(this)">
    <table id="tabelaLista">
        <thead>
            <tr>
                <th>Tabela</th>
                <th>Total de Indexes</th>
            </tr>
        </thead>
        <tbody>
            {linhas}
        </tbody>
    </table>
    """

    template = lerTemplate("base.html")
    html = renderizar(template, {
        "titulo": "Indexes",
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/indexes/index.html", html)
    print("indexes/index.html gerado.")
    return tabelas


def gerarPaginaTabelaIndexes(schema, tabela, indexes):
    indexes_html = ""
    for i in indexes:
        tag = "tag-valid" if i['status'] == "VALID" else "tag-invalid"

        colunas_html = ""
        for col in i["colunas"]:
            colunas_html += f"""
            <tr>
                <td>{col['nome']}</td>
                <td>{col['posicao']}</td>
                <td>{col['ordem']}</td>
            </tr>
            """

        indexes_html += f"""
        <div class="card">
            <h3>{i['nome']}</h3>
            <table>
                <tbody>
                    <tr><td><strong>Tipo</strong></td><td>{i['tipo']}</td></tr>
                    <tr><td><strong>Único</strong></td><td>{i['unico']}</td></tr>
                    <tr><td><strong>Status</strong></td><td><span class="tag {tag}">{i['status']}</span></td></tr>
                </tbody>
            </table>

            <h3 style="margin-top: 16px;">Colunas</h3>
            <table>
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Posição</th>
                        <th>Ordem</th>
                    </tr>
                </thead>
                <tbody>
                    {colunas_html}
                </tbody>
            </table>
        </div>
        """

    conteudo = f"""
    <div class="card">
        <h3>Tabela: {tabela}</h3>
        <p style="color: #555; margin-top: 8px;">Total de indexes: {len(indexes)}</p>
    </div>
    {indexes_html}
    """

    template = lerTemplate("base.html")
    html = renderizar(template, {
        "titulo": f"Indexes — {tabela}",
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/indexes/{tabela.lower()}.html", html)


def gerarIndexes(schema_data):
    schema = schema_data["schema"]
    tabelas = gerarListaIndexes(schema_data)

    for tabela, indexes in tabelas.items():
        gerarPaginaTabelaIndexes(schema, tabela, indexes)

    print(f"{len(tabelas)} páginas de indexes geradas.")