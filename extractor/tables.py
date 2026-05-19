def extrairTabela(cursor):
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

        # conta registros reais
        cursor2 = cursor.connection.cursor()
        cursor2.execute(f"SELECT COUNT(*) FROM {nome}")
        total = cursor2.fetchone()[0]
        cursor2.close()

        tabelas.append({
            "nome": nome,
            "status": status,
            "num_rows": total
        })

    return tabelas
