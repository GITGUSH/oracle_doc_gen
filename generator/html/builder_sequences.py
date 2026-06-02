from generator.html.builder import lerTemplate, renderizar, salvarArquivo, linkObjeto

def gerarListaSequences(schema_data):
    schema = schema_data["schema"]
    sequences = schema_data["sequences"]

    linhas = ""
    for s in sequences:
        linhas += f"""
        <tr>
            <td><a href="{s['nome'].lower()}.html">{s['nome']}</a></td>
            <td>{s['incremento']}</td>
            <td>{s['ultimo_valor']}</td>
            <td>{s['ciclico']}</td>
            <td>{s['cache']}</td>
        </tr>
        """

    conteudo = f"""
    <input type="text" class="search-box" placeholder="Buscar sequence..." onkeyup="filtrarTabela(this)">
    <table id="tabelaLista">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Incremento</th>
                <th>Último Valor</th>
                <th>Cíclico</th>
                <th>Cache</th>
            </tr>
        </thead>
        <tbody>
            {linhas}
        </tbody>
    </table>
    """

    template = lerTemplate("base.html")
    html = renderizar(template, {
        "titulo": "Sequences",
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "active_sequences": "active",
        "breadcrumb": f"<a href='../../index_{schema}.html'>Início</a> › Sequences",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/sequences/index.html", html)
    print("sequences/index.html gerado.")


def gerarPaginaSequence(schema, sequence):
    conteudo = f"""
    <div class="card">
        <h3>Informações Gerais</h3>
        <table>
            <tbody>
                <tr><td><strong>Nome</strong></td><td>{sequence['nome']}</td></tr>
                <tr><td><strong>Valor Mínimo</strong></td><td>{sequence['valor_minimo']}</td></tr>
                <tr><td><strong>Valor Máximo</strong></td><td>{sequence['valor_maximo']}</td></tr>
                <tr><td><strong>Incremento</strong></td><td>{sequence['incremento']}</td></tr>
                <tr><td><strong>Último Valor</strong></td><td>{sequence['ultimo_valor']}</td></tr>
                <tr><td><strong>Cíclico</strong></td><td>{sequence['ciclico']}</td></tr>
                <tr><td><strong>Ordenado</strong></td><td>{sequence['ordenado']}</td></tr>
                <tr><td><strong>Cache</strong></td><td>{sequence['cache']}</td></tr>
            </tbody>
        </table>
    </div>
    """

    template = lerTemplate("base.html")
    pagina_html = renderizar(template, {
        "titulo": sequence['nome'],
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "active_sequences": "active",
        "breadcrumb": f"<a href='../../index_{schema}.html'>Início</a> › <a href='index.html'>Sequences</a> › {sequence['nome']}",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/sequences/{sequence['nome'].lower()}.html", pagina_html)


def gerarSequences(schema_data):
    schema = schema_data["schema"]
    gerarListaSequences(schema_data)

    for sequence in schema_data["sequences"]:
        gerarPaginaSequence(schema, sequence)

    print(f"{len(schema_data['sequences'])} páginas de sequences geradas.")