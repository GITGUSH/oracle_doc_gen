def extrairTriggers(cursor):
    cursor.execute("""
        SELECT
            t.trigger_name,
            t.trigger_type,
            t.triggering_event,
            t.table_name,
            t.status,
            o.last_ddl_time
        FROM user_triggers t
        JOIN user_objects o
            ON o.object_name = t.trigger_name
            AND o.object_type = 'TRIGGER'
        ORDER BY t.trigger_name
    """)

    triggers = []
    for row in cursor.fetchall():
        nome = row[0]

        # código fonte
        cursor2 = cursor.connection.cursor()
        cursor2.execute("""
            SELECT text
            FROM user_source
            WHERE name = :nome
              AND type = 'TRIGGER'
            ORDER BY line
        """, nome=nome)

        codigo = "".join([l[0] for l in cursor2.fetchall()])
        cursor2.close()

        # dependências
        cursor3 = cursor.connection.cursor()
        cursor3.execute("""
            SELECT
                referenced_name,
                referenced_type
            FROM user_dependencies
            WHERE name = :nome
              AND type = 'TRIGGER'
            ORDER BY referenced_name
        """, nome=nome)

        dependencias = []
        for dep in cursor3.fetchall():
            dependencias.append({
                "nome": dep[0],
                "tipo": dep[1]
            })
        cursor3.close()

        triggers.append({
            "nome": nome,
            "tipo": row[1],
            "evento": row[2],
            "tabela": row[3],
            "status": row[4],
            "ultima_alteracao": row[5],
            "codigo": codigo,
            "dependencias": dependencias
        })

    return triggers