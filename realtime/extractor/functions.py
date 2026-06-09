def extrairDependenciasFunction(cursor, nome_function):
    cursor.execute("""
        SELECT
            referenced_name,
            referenced_type
        FROM user_dependencies
        WHERE name = :nome
          AND type = 'FUNCTION'
        ORDER BY referenced_name
    """, nome=nome_function)

    dependencias = []
    for row in cursor.fetchall():
        dependencias.append({
            "nome": row[0],
            "tipo": row[1]
        })

    return dependencias


def extrairFunctions(cursor):
    cursor.execute("""
        SELECT
            object_name,
            status,
            last_ddl_time
        FROM user_objects
        WHERE object_type = 'FUNCTION'
        ORDER BY object_name
    """)

    functions = []
    for row in cursor.fetchall():
        nome = row[0]

        # código fonte
        cursor2 = cursor.connection.cursor()
        cursor2.execute("""
            SELECT text
            FROM user_source
            WHERE name = :nome
              AND type = 'FUNCTION'
            ORDER BY line
        """, nome=nome)

        codigo = "".join([l[0] for l in cursor2.fetchall()])
        cursor2.close()

        # argumentos
        cursor3 = cursor.connection.cursor()
        cursor3.execute("""
            SELECT
                argument_name,
                data_type,
                in_out,
                position
            FROM user_arguments
            WHERE object_name = :nome
            ORDER BY position
        """, nome=nome)

        argumentos = []
        for arg in cursor3.fetchall():
            argumentos.append({
                "nome": arg[0],
                "tipo": arg[1],
                "direcao": arg[2],
                "posicao": arg[3]
            })
        cursor3.close()

        functions.append({
            "nome": nome,
            "status": row[1],
            "ultima_alteracao": row[2],
            "codigo": codigo,
            "argumentos": argumentos,
            "dependencias": extrairDependenciasFunction(cursor, nome)
        })

    return functions