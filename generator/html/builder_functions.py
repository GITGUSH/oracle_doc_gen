from generator.html.builder import lerTemplate, renderizar, salvarArquivo, linkObjeto
import html

def gerarListaFunctions(schema_data):
    schema = schema_data["schema"]
    functions = schema_data["functions"]

    linhas = ""
    for f in functions:
        tag = "tag-valid" if f['status'] == "VALID" else "tag-invalid"
        linhas += f"""
        <tr>
            <td><a href="{f['nome'].lower()}.html">{f['nome']}</a></td>
            <td>{len(f['argumentos'])}</td>
            <td>{len(f['dependencias'])}</td>
            <td><span class="tag {tag}">{f['status']}</span></td>
        </tr>
        """

    conteudo = f"""
    <input type="text" class="search-box" placeholder="Buscar function..." onkeyup="filtrarTabela(this)">
    <table id="tabelaLista">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Argumentos</th>
                <th>Dependências</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {linhas}
        </tbody>
    </table>
    """

    template = lerTemplate("base.html")
    html = renderizar(template, {
        "titulo": "Functions",
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/functions/index.html", html)
    print("functions/index.html gerado.")


def gerarPaginaFunction(schema, function):
    codigo_fonte = html.escape(function['codigo'])

    args_html = ""
    for arg in function["argumentos"]:
        nome = "RETURN" if arg['nome'] is None else arg['nome']
        args_html += f"""
        <tr>
            <td>{nome}</td>
            <td>{arg['tipo'] or '-'}</td>
            <td><span class="tag tag-pk">{arg['direcao']}</span></td>
            <td>{arg['posicao']}</td>
        </tr>
        """

    deps_html = ""
    for dep in function["dependencias"]:
        deps_html += f"""
        <tr>
            <td>{linkObjeto(dep['nome'], dep['tipo'], '..')}</td>
            <td>{dep['tipo']}</td>
        </tr>
        """

    conteudo = f"""
    <div class="card">
        <h3>Informações Gerais</h3>
        <table>
            <tbody>
                <tr><td><strong>Nome</strong></td><td>{function['nome']}</td></tr>
                <tr><td><strong>Status</strong></td><td>{function['status']}</td></tr>
                <tr><td><strong>Última Alteração</strong></td><td>{function['ultima_alteracao']}</td></tr>
            </tbody>
        </table>
    </div>

    <div class="card">
        <h3>Argumentos</h3>
        <table>
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Tipo</th>
                    <th>Direção</th>
                    <th>Posição</th>
                </tr>
            </thead>
            <tbody>
                {args_html}
            </tbody>
        </table>
    </div>

    <div class="card">
        <h3>Dependências</h3>
        <table>
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Tipo</th>
                </tr>
            </thead>
            <tbody>
                {deps_html}
            </tbody>
        </table>
    </div>

    <div class="card">
        <h3>Código Fonte</h3>
        <pre>{codigo_fonte}</pre>
    </div>
    """

    template = lerTemplate("base.html")
    pagina_html = renderizar(template, {
        "titulo": function['nome'],
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/functions/{function['nome'].lower()}.html", pagina_html)


def gerarFunctions(schema_data):
    schema = schema_data["schema"]
    gerarListaFunctions(schema_data)

    for function in schema_data["functions"]:
        gerarPaginaFunction(schema, function)

    print(f"{len(schema_data['functions'])} páginas de functions geradas.")