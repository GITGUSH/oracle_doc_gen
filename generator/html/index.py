from generator.html.builder import lerTemplate, renderizar, salvarArquivo

def gerarIndex(schema_data):
    schema = schema_data["schema"]

    # coleta objetos inválidos
    invalidos = []

    for t in schema_data["tabelas"]:
        if t["status"] != "VALID":
            invalidos.append({"nome": t["nome"], "tipo": "Tabela"})

    for v in schema_data["views"]:
        if v.get("status", "VALID") != "VALID":
            invalidos.append({"nome": v["nome"], "tipo": "View"})

    for p in schema_data["procedures"]:
        if p["status"] != "VALID":
            invalidos.append({"nome": p["nome"], "tipo": "Procedure"})

    for f in schema_data["functions"]:
        if f["status"] != "VALID":
            invalidos.append({"nome": f["nome"], "tipo": "Function"})

    for p in schema_data["packages"]:
        if p["status"] != "VALID":
            invalidos.append({"nome": p["nome"], "tipo": "Package"})

    for t in schema_data["triggers"]:
        if t["status"] != "ENABLED":
            invalidos.append({"nome": t["nome"], "tipo": "Trigger"})

    # card de invalidos
    if invalidos:
        linhas_invalidos = ""
        for obj in invalidos:
            linhas_invalidos += f"""
            <tr>
                <td>{obj['nome']}</td>
                <td>{obj['tipo']}</td>
                <td><span class="tag tag-invalid">INVALID</span></td>
            </tr>
            """
        card_invalidos = f"""
        <div class="card">
            <h3>Objetos que Requerem Atencao</h3>
            <table>
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Tipo</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {linhas_invalidos}
                </tbody>
            </table>
        </div>
        """
    else:
        card_invalidos = """
        <div class="card">
            <h3>Objetos Inválidos</h3>
            <p style="color: #065F46; font-weight: bold;">Nenhum objeto invalido encontrado.</p>
        </div>
        """

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

    {card_invalidos}
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