from generator.html.builder import lerTemplate, renderizar, salvarArquivo, linkObjeto

def gerarListaJobs(schema_data):
    schema = schema_data["schema"]
    jobs = schema_data["jobs"]

    linhas = ""
    for j in jobs:
        tag = "tag-valid" if j['habilitado'] == "Sim" else "tag-invalid"
        linhas += f"""
        <tr>
            <td><a href="{j['nome'].lower()}.html">{j['nome']}</a></td>
            <td>{j['tipo']}</td>
            <td>{j['estado']}</td>
            <td>{j['proxima_execucao']}</td>
            <td><span class="tag {tag}">{j['habilitado']}</span></td>
        </tr>
        """

    conteudo = f"""
    <input type="text" class="search-box" placeholder="Buscar job..." onkeyup="filtrarTabela(this)">
    <table id="tabelaLista">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Tipo</th>
                <th>Estado</th>
                <th>Próxima Execução</th>
                <th>Habilitado</th>
            </tr>
        </thead>
        <tbody>
            {linhas}
        </tbody>
    </table>
    """

    template = lerTemplate("base.html")
    html = renderizar(template, {
        "titulo": "Jobs",
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "active_jobs": "active",
        "breadcrumb": "<a href='../..'>Início</a> › Jobs",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/jobs/index.html", html)
    print("jobs/index.html gerado.")


def gerarPaginaJob(schema, job):
    conteudo = f"""
    <div class="card">
        <h3>Informações Gerais</h3>
        <table>
            <tbody>
                <tr><td><strong>Nome</strong></td><td>{job['nome']}</td></tr>
                <tr><td><strong>Tipo</strong></td><td>{job['tipo']}</td></tr>
                <tr><td><strong>Estado</strong></td><td>{job['estado']}</td></tr>
                <tr><td><strong>Habilitado</strong></td><td>{job['habilitado']}</td></tr>
                <tr><td><strong>Data Início</strong></td><td>{job['data_inicio']}</td></tr>
                <tr><td><strong>Data Fim</strong></td><td>{job['data_fim'] or '-'}</td></tr>
                <tr><td><strong>Intervalo</strong></td><td>{job['intervalo'] or '-'}</td></tr>
                <tr><td><strong>Última Execução</strong></td><td>{job['ultima_execucao'] or '-'}</td></tr>
                <tr><td><strong>Duração Última</strong></td><td>{job['duracao_ultima'] or '-'}</td></tr>
                <tr><td><strong>Próxima Execução</strong></td><td>{job['proxima_execucao'] or '-'}</td></tr>
                <tr><td><strong>Execuções</strong></td><td>{job['qtd_execucoes']}</td></tr>
                <tr><td><strong>Falhas</strong></td><td>{job['qtd_falhas']}</td></tr>
                <tr><td><strong>Comentários</strong></td><td>{job['comentarios'] or '-'}</td></tr>
            </tbody>
        </table>
    </div>

    <div class="card">
        <h3>Ação</h3>
        <pre>{job['acao']}</pre>
    </div>
    """

    template = lerTemplate("base.html")
    html = renderizar(template, {
        "titulo": job['nome'],
        "schema": schema,
        "caminho_assets": "../../assets",
        "caminho_raiz": "../..",
        "active_jobs": "active",
        "breadcrumb": f"<a href='../..'>Início</a> › <a href='index.html'>Jobs</a> › {job['nome']}",
        "conteudo": conteudo
    })

    salvarArquivo(f"output/{schema}/jobs/{job['nome'].lower()}.html", html)


def gerarJobs(schema_data):
    schema = schema_data["schema"]
    gerarListaJobs(schema_data)

    for job in schema_data["jobs"]:
        gerarPaginaJob(schema, job)

    print(f"{len(schema_data['jobs'])} páginas de jobs geradas.")