def extrairColunas(cursor, nome_tabela):
    cursor.execute("""
        SELECT 
            column_name,
            data_type,
            data_length,
            data_precision,
            data_scale,
            nullable,
            data_default
        FROM user_tab_columns
        WHERE table_name = :tabela
        ORDER BY column_id
    """, tabela=nome_tabela)

    colunas = []
    for row in cursor.fetchall():
        colunas.append({
            "nome": row[0],
            "tipo": row[1],
            "tamanho": row[2],
            "precisao": row[3],
            "escala": row[4],
            "nulavel": "Sim" if row[5] == "Y" else "Não",
            "default": row[6]
        })
    return colunas 


def extrairTabelas(cursor):
    cursor.execute("""
        SELECT
            table_name,
            num_rows,
            status
        FROM user_tables
        ORDER BY table_name
    """)

    tabelas = []

    for row in cursor.fetchall():
        nome = row[0]
        status = row[1]

        # conta registros das tabelas
        cursor2 = cursor.connection.cursor()
        cursor2.execute(f"SELECT COUNT(*) FROM {nome}")
        total = cursor2.fetchone()[0]
        cursor2.close()

        colunas = extrairColunas(cursor, nome)
        
        tabelas.append({
            "nome": nome,
            "status": status,
            "num_rows": total,
            "colunas": colunas
        })

    return tabelas
