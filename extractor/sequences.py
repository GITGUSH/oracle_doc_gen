def extrairSequences(cursor):
    cursor.execute("""
        SELECT
            sequence_name,
            min_value,
            max_value,
            increment_by,
            cycle_flag,
            order_flag,
            cache_size,
            last_number
        FROM user_sequences
        ORDER BY sequence_name
    """)

    sequences = []
    for row in cursor.fetchall():
        sequences.append({
            "nome": row[0],
            "valor_minimo": row[1],
            "valor_maximo": row[2],
            "incremento": row[3],
            "ciclico": "Sim" if row[4] == "Y" else "Não",
            "ordenado": "Sim" if row[5] == "Y" else "Não",
            "cache": row[6],
            "ultimo_valor": row[7]
        })

    return sequences