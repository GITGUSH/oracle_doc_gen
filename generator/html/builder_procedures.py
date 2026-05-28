from generator.html.builder import lerTemplate, renderizar, salvarArquivo
import html

def gerarListaProcedures(schema_data):
    schema = schema_data["schema"]
    procedures = schema_data["procedures"]

    linhas = ""
    for p in procedures:
        tag = "tag-valid" if p['status'] == "VALID" else "tag-invalid"
        linhas += f"""
        <tr>
            <td><a href="{p['nome'].lower()}.html">{p['nome']}</a></td>
            <td>{len(p['argumentos'])}</td>
            <td>{len(p['dependencias'])}</td>
            <td><span class="tag {tag}">{p['status']}</span></td>
        </tr>
        """

    conteudo = f"""
    <input type="text" class="search-box" placeholder="Buscar procedure..." onkeyup="filtrarTabela(this)">
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
        "titulo": "Procedures",
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/procedures/index.html", html)
    print("procedures/index.html gerado.")


def gerarPaginaProcedure(schema, procedure):
    codigo_fonte = html.escape(procedure['codigo'])

    args_html = ""
    for arg in procedure["argumentos"]:
        args_html += f"""
        <tr>
            <td>{arg['nome'] or '-'}</td>
            <td>{arg['tipo'] or '-'}</td>
            <td><span class="tag tag-pk">{arg['direcao']}</span></td>
            <td>{arg['posicao']}</td>
        </tr>
        """

    deps_html = ""
    for dep in procedure["dependencias"]:
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
                <tr><td><strong>Nome</strong></td><td>{procedure['nome']}</td></tr>
                <tr><td><strong>Status</strong></td><td>{procedure['status']}</td></tr>
                <tr><td><strong>Última Alteração</strong></td><td>{procedure['ultima_alteracao']}</td></tr>
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
        "titulo": procedure['nome'],
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/procedures/{procedure['nome'].lower()}.html", pagina_html)


def gerarProcedures(schema_data):
    schema = schema_data["schema"]
    gerarListaProcedures(schema_data)

    for procedure in schema_data["procedures"]:
        gerarPaginaProcedure(schema, procedure)

    print(f"{len(schema_data['procedures'])} páginas de procedures geradas.")