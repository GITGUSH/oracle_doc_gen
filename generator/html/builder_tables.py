from generator.html.builder import lerTemplate, renderizar, salvarArquivo, linkObjeto
from generator.plantuml import gerarCodigoPuml, gerarUrlDiagrama

def gerarListaTabelas(schema_data):
    schema = schema_data["schema"]
    tabelas = schema_data["tabelas"]

    linhas = ""
    for t in tabelas:
        linhas += f"""
        <tr>
            <td><a href="{t['nome'].lower()}.html">{t['nome']}</a></td>
            <td>{t['num_rows']}</td>
            <td>{len(t['colunas'])}</td>
            <td><span class="tag tag-valid">{t['status']}</span></td>
        </tr>
        """

    conteudo = f"""
    <input type="text" class="search-box" placeholder="Buscar tabela..." onkeyup="filtrarTabela(this)">
    <table id="tabelaLista">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Registros</th>
                <th>Colunas</th>
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
        "titulo": "Tabelas",
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/tables/index.html", html)
    print("tables/index.html gerado.")


def gerarPaginaTabela(schema, tabela, todas_tabelas):
    codigo_puml = gerarCodigoPuml(tabela, todas_tabelas)
    url_diagrama = gerarUrlDiagrama(codigo_puml)

    colunas_html = ""
    for col in tabela["colunas"]:
        colunas_html += f"""
        <tr>
            <td>{col['nome']}</td>
            <td>{col['tipo']}</td>
            <td>{col['tamanho'] or '-'}</td>
            <td>{col['nulavel']}</td>
            <td>{col['default'] or '-'}</td>
        </tr>
        """

    constraints_html = ""
    for c in tabela["constraints"]:
        tipo_tag = "tag-pk" if c['tipo'] == 'PK' else "tag-fk"
        ref = f"→ {linkObjeto(c['tabela_ref'], 'TABLE', '..')}" if c['tipo'] == 'FK' else ""
        constraints_html += f"""
        <tr>
            <td><span class="tag {tipo_tag}">{c['tipo']}</span></td>
            <td>{c['coluna']}</td>
            <td>{ref}</td>
        </tr>
        """

    conteudo = f"""
    <div class="card">
        <h3>Informações Gerais</h3>
        <table>
            <tbody>
                <tr><td><strong>Nome</strong></td><td>{tabela['nome']}</td></tr>
                <tr><td><strong>Registros</strong></td><td>{tabela['num_rows']}</td></tr>
                <tr><td><strong>Status</strong></td><td>{tabela['status']}</td></tr>
            </tbody>
        </table>
    </div>

    <div class="card">
        <h3>Colunas</h3>
        <table>
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Tipo</th>
                    <th>Tamanho</th>
                    <th>Nulável</th>
                    <th>Default</th>
                </tr>
            </thead>
            <tbody>
                {colunas_html}
            </tbody>
        </table>
    </div>

    <div class="card">
        <h3>Constraints</h3>
        <table>
            <thead>
                <tr>
                    <th>Tipo</th>
                    <th>Coluna</th>
                    <th>Referência</th>
                </tr>
            </thead>
            <tbody>
                {constraints_html}
            </tbody>
        </table>
    </div>

    <div class="card">
        <h3>Diagrama de Relacionamentos</h3>
        <div style="text-align: center; padding: 20px;">
            <img src="{url_diagrama}" alt="Diagrama {tabela['nome']}" style="max-width: 100%;">
        </div>
        <details style="margin-top: 16px;">
            <summary style="cursor: pointer; color: #1E2761; font-weight: bold;">Ver código PlantUML</summary>
            <pre style="margin-top: 12px;">{codigo_puml}</pre>
        </details>
    </div>
    """

    template = lerTemplate("base.html")
    pagina_html = renderizar(template, {
        "titulo": tabela['nome'],
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/tables/{tabela['nome'].lower()}.html", pagina_html)


def gerarTabelas(schema_data):
    schema = schema_data["schema"]
    gerarListaTabelas(schema_data)

    for tabela in schema_data["tabelas"]:
        gerarPaginaTabela(schema, tabela, schema_data["tabelas"])

    print(f"{len(schema_data['tabelas'])} páginas de tabelas geradas.")