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

def extrairConstraints(cursor, nome_tabela):
    cursor.execute("""
        SELECT
            c.constraint_name,
            c.constraint_type,
            cc.column_name,
            c.r_constraint_name,
            rc.table_name as tabela_referenciada
        FROM user_constraints c
        JOIN user_cons_columns cc 
            ON c.constraint_name = cc.constraint_name
        LEFT JOIN user_constraints rc 
            ON c.r_constraint_name = rc.constraint_name
        WHERE c.table_name = :tabela
          AND c.constraint_type IN ('P', 'R')
        ORDER BY c.constraint_type, cc.position
    """, tabela=nome_tabela)

    constraints = []

    for row in cursor.fetchall():
        constraints.append({
            "nome": row[0],
            "tipo": "PK" if row[1] == "P" else "FK",
            "coluna": row[2],
            "ref_constraint": row[3],
            "tabela_ref": row[4]
        })
    
    return constraints


def extrairTabelas(cursor):
    cursor.execute("""
        SELECT
            t.table_name,
            o.status
        FROM user_tables t
        JOIN user_objects o
            ON o.object_name = t.table_name
            AND o.object_type = 'TABLE'
        ORDER BY t.table_name
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
            "colunas": colunas,
            "constraints": extrairConstraints(cursor, nome) #Appenda as constraints nas tabelas
        })

    return tabelas
