from generator.html.builder import lerTemplate, renderizar, salvarArquivo

def gerarIndex(schema_data):
    schema = schema_data["schema"]

    conteudo = f"""
    <div class="card">
        <h3>Resumo do Schema {schema}</h3>
        <table>
            <thead>
                <tr>
                    <th>Objeto</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Tabelas</td><td>{len(schema_data['tabelas'])}</td></tr>
                <tr><td>Views</td><td>{len(schema_data['views'])}</td></tr>
                <tr><td>Procedures</td><td>{len(schema_data['procedures'])}</td></tr>
                <tr><td>Functions</td><td>{len(schema_data['functions'])}</td></tr>
                <tr><td>Packages</td><td>{len(schema_data['packages'])}</td></tr>
                <tr><td>Triggers</td><td>{len(schema_data['triggers'])}</td></tr>
                <tr><td>Sequences</td><td>{len(schema_data['sequences'])}</td></tr>
                <tr><td>Indexes</td><td>{len(schema_data['indexes'])}</td></tr>
                <tr><td>Synonyms</td><td>{len(schema_data['synonyms'])}</td></tr>
                <tr><td>Jobs</td><td>{len(schema_data['jobs'])}</td></tr>
            </tbody>
        </table>
    </div>
    """

    template = lerTemplate("base.html")
    html = renderizar(template, {
        "titulo": f"Documentação — {schema}",
        "schema": schema,
        "caminho_assets": "assets",
        "caminho_raiz": ".",
        "active_inicio": "active",
        "breadcrumb": "Início",
        "conteudo": conteudo
    })
    salvarArquivo("output/index.html", html)
    print("index.html gerado.")