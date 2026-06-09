def extrairJobs(cursor):
    cursor.execute("""
        SELECT
            job_name,
            job_type,
            job_action,
            start_date,
            repeat_interval,
            end_date,
            enabled,
            state,
            run_count,
            failure_count,
            last_start_date,
            last_run_duration,
            next_run_date,
            comments
        FROM user_scheduler_jobs
        ORDER BY job_name
    """)

    jobs = []
    for row in cursor.fetchall():
        jobs.append({
            "nome": row[0],
            "tipo": row[1],
            "acao": row[2],
            "data_inicio": row[3],
            "intervalo": row[4],
            "data_fim": row[5],
            "habilitado": "Sim" if row[6] == "TRUE" else "Não",
            "estado": row[7],
            "qtd_execucoes": row[8],
            "qtd_falhas": row[9],
            "ultima_execucao": row[10],
            "duracao_ultima": row[11],
            "proxima_execucao": row[12],
            "comentarios": row[13]
        })

    return jobs