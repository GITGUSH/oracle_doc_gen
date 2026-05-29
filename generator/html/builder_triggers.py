from generator.html.builder import lerTemplate, renderizar, salvarArquivo
import html

def gerarListaTriggers(schema_data):
    schema = schema_data["schema"]
    triggers = schema_data["triggers"]

    linhas = ""
    for t in triggers:
        tag = "tag-valid" if t['status'] == "ENABLED" else "tag-invalid"
        linhas += f"""
        <tr>
            <td><a href="{t['nome'].lower()}.html">{t['nome']}</a></td>
            <td>{t['tabela']}</td>
            <td>{t['evento']}</td>
            <td>{t['tipo']}</td>
            <td><span class="tag {tag}">{t['status']}</span></td>
        </tr>
        """

    conteudo = f"""
    <input type="text" class="search-box" placeholder="Buscar trigger..." onkeyup="filtrarTabela(this)">
    <table id="tabelaLista">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Tabela</th>
                <th>Evento</th>
                <th>Tipo</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {linhas}
        </tbody>
    </table>
    """

    template = lerTemplate("base.html")
    pagina_html = renderizar(template, {
        "titulo": "Triggers",
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/triggers/index.html", pagina_html)
    print("triggers/index.html gerado.")


def gerarPaginaTrigger(schema, trigger):
    codigo_fonte = html.escape(trigger['codigo'])

    deps_html = ""
    for dep in trigger["dependencias"]:
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
                <tr><td><strong>Nome</strong></td><td>{trigger['nome']}</td></tr>
                <tr><td><strong>Tabela</strong></td><td>{trigger['tabela']}</td></tr>
                <tr><td><strong>Evento</strong></td><td>{trigger['evento']}</td></tr>
                <tr><td><strong>Tipo</strong></td><td>{trigger['tipo']}</td></tr>
                <tr><td><strong>Status</strong></td><td>{trigger['status']}</td></tr>
                <tr><td><strong>Última Alteração</strong></td><td>{trigger['ultima_alteracao']}</td></tr>
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
        "titulo": trigger['nome'],
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/triggers/{trigger['nome'].lower()}.html", pagina_html)


def gerarTriggers(schema_data):
    schema = schema_data["schema"]
    gerarListaTriggers(schema_data)

    for trigger in schema_data["triggers"]:
        gerarPaginaTrigger(schema, trigger)

    print(f"{len(schema_data['triggers'])} páginas de triggers geradas.")