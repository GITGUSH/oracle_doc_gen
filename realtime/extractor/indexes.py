def extrairColunasIndex(cursor, nome_index):
    cursor2 = cursor.connection.cursor()
    cursor2.execute("""
        SELECT
            column_name,
            column_position,
            descend
        FROM user_ind_columns
        WHERE index_name = :nome_index
        ORDER BY column_position
    """, nome_index=nome_index)

    colunas = []
    for row in cursor2.fetchall():
        colunas.append({
            "nome": row[0],
            "posicao": row[1],
            "ordem": row[2]
        })

    cursor2.close()
    return colunas


def extrairIndexes(cursor):
    cursor.execute("""
        SELECT
            index_name,
            table_name,
            index_type,
            uniqueness,
            status
        FROM user_indexes
        ORDER BY table_name, index_name
    """)

    indexes = []
    for row in cursor.fetchall():
        nome = row[0]

        indexes.append({
            "nome": nome,
            "tabela": row[1],
            "tipo": row[2],
            "unico": "Sim" if row[3] == "UNIQUE" else "Não",
            "status": row[4],
            "colunas": extrairColunasIndex(cursor, nome)
        })

    return indexes