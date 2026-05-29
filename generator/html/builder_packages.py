from generator.html.builder import lerTemplate, renderizar, salvarArquivo
import html

def gerarListaPackages(schema_data):
    schema = schema_data["schema"]
    packages = schema_data["packages"]

    linhas = ""
    for p in packages:
        tag = "tag-valid" if p['status'] == "VALID" else "tag-invalid"
        linhas += f"""
        <tr>
            <td><a href="{p['nome'].lower()}.html">{p['nome']}</a></td>
            <td>{len(p['subprogramas'])}</td>
            <td>{len(p['dependencias'])}</td>
            <td><span class="tag {tag}">{p['status']}</span></td>
        </tr>
        """

    conteudo = f"""
    <input type="text" class="search-box" placeholder="Buscar package..." onkeyup="filtrarTabela(this)">
    <table id="tabelaLista">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Subprogramas</th>
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
        "titulo": "Packages",
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/packages/index.html", html)
    print("packages/index.html gerado.")


def gerarPaginaPackage(schema, package):
    header_fonte = html.escape(package['header'])
    body_fonte = html.escape(package['body'])

    subs_html = ""
    for sub in package["subprogramas"]:
        args_html = ""
        for arg in sub["argumentos"]:
            nome = "RETURN" if arg['nome'] is None else arg['nome']
            args_html += f"""
            <tr>
                <td>{nome}</td>
                <td>{arg['tipo'] or '-'}</td>
                <td><span class="tag tag-pk">{arg['direcao']}</span></td>
                <td>{arg['posicao']}</td>
            </tr>
            """

        subs_html += f"""
        <div class="card">
            <h3>{sub['nome']}</h3>
            <table>
                <thead>
                    <tr>
                        <th>Argumento</th>
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
        """

    deps_html = ""
    for dep in package["dependencias"]:
        deps_html += f"""
        <tr>
            <td>{dep['nome']}</td>
            <td>{dep['tipo']}</td>
        </tr>
        """

    conteudo = f"""
    <div class="card">
        <h3>Informações Gerais</h3>
        <table>
            <tbody>
                <tr><td><strong>Nome</strong></td><td>{package['nome']}</td></tr>
                <tr><td><strong>Status</strong></td><td>{package['status']}</td></tr>
                <tr><td><strong>Última Alteração</strong></td><td>{package['ultima_alteracao']}</td></tr>
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

    <h3 style="margin: 24px 0 12px; color: #1E2761;">Subprogramas</h3>
    {subs_html}

    <div class="card">
        <h3>Header</h3>
        <pre>{header_fonte}</pre>
    </div>

    <div class="card">
        <h3>Body</h3>
        <pre>{body_fonte}</pre>
    </div>
    """

    template = lerTemplate("base.html")
    pagina_html = renderizar(template, {
        "titulo": package['nome'],
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/packages/{package['nome'].lower()}.html", pagina_html)


def gerarPackages(schema_data):
    schema = schema_data["schema"]
    gerarListaPackages(schema_data)

    for package in schema_data["packages"]:
        gerarPaginaPackage(schema, package)

    print(f"{len(schema_data['packages'])} páginas de packages geradas.")