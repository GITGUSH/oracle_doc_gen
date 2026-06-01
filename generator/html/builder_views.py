from generator.html.builder import lerTemplate, renderizar, salvarArquivo, linkObjeto
import html

def gerarListaViews(schema_data):
    schema = schema_data["schema"]
    views = schema_data["views"]

    linhas = ""
    for v in views:
        linhas += f"""
        <tr>
            <td><a href="{v['nome'].lower()}.html">{v['nome']}</a></td>
            <td>{len(v['colunas'])}</td>
            <td>{len(v['dependencias'])}</td>
        </tr>
        """

    conteudo = f"""
    <input type="text" class="search-box" placeholder="Buscar view..." onkeyup="filtrarTabela(this)">
    <table id="tabelaLista">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Colunas</th>
                <th>Dependências</th>
            </tr>
        </thead>
        <tbody>
            {linhas}
        </tbody>
    </table>
    """

    template = lerTemplate("base.html")
    html = renderizar(template, {
        "titulo": "Views",
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "active_views": "active",
        "breadcrumb": "<a href='../..'>Início</a> › Views",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/views/index.html", html)
    print("views/index.html gerado.")


def gerarPaginaView(schema, view):
    codigo_fonte = html.escape(view['codigo'])  # Views geralmente não têm código fonte como procedures, mas vamos mostrar a definição SQL

    colunas_html = ""
    for col in view["colunas"]:
        colunas_html += f"""
        <tr>
            <td>{col['nome']}</td>
            <td>{col['tipo']}</td>
            <td>{col['tamanho'] or '-'}</td>
            <td>{col['nulavel']}</td>
        </tr>
        """

    deps_html = ""
    for dep in view["dependencias"]:
        deps_html += f"""
        <tr>
            <td>{linkObjeto(dep['nome'], dep['tipo'], '..')}</td>
            <td>{dep['tipo']}</td>
        </tr>
        """

    conteudo = f"""
    <div class="card">
        <h3>Colunas</h3>
        <table>
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Tipo</th>
                    <th>Tamanho</th>
                    <th>Nulável</th>
                </tr>
            </thead>
            <tbody>
                {colunas_html}
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
        <pre><code class="language-sql">{codigo_fonte}</code></pre>
    </div>
    """

    template = lerTemplate("base.html")
    pagina_html = renderizar(template, {
        "titulo": view['nome'],
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "active_views": "active",
        "breadcrumb": f"<a href='../..'>Início</a> › <a href='index.html'>Views</a> › {view['nome']}",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/views/{view['nome'].lower()}.html", pagina_html)


def gerarViews(schema_data):
    schema = schema_data["schema"]
    gerarListaViews(schema_data)

    for view in schema_data["views"]:
        gerarPaginaView(schema, view)

    print(f"{len(schema_data['views'])} páginas de views geradas.")