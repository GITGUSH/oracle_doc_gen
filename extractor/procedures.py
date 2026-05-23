def extrairDependenciasProcedure(cursor, nome_procedure):
    cursor.execute("""
        SELECT
            referenced_name,
            referenced_type
        FROM user_dependencies
        WHERE name = :nome
          AND type = 'PROCEDURE'
        ORDER BY referenced_name
    """, nome=nome_procedure)

    dependencias = []
    for row in cursor.fetchall():
        dependencias.append({
            "nome": row[0],
            "tipo": row[1]
        })

    return dependencias


def extrairArgumentos(cursor, nome_procedure):
    cursor.execute("""
        SELECT
            argument_name,
            data_type,
            in_out,
            position
        FROM user_arguments
        WHERE object_name = :nome
        ORDER BY position
    """, nome=nome_procedure)

    argumentos = []
    for row in cursor.fetchall():
        argumentos.append({
            "nome": row[0],
            "tipo": row[1],
            "direcao": row[2],
            "posicao": row[3]
        })

    return argumentos


def extrairProcedures(cursor):
    cursor.execute("""
        SELECT
            object_name,
            status,
            last_ddl_time
        FROM user_objects
        WHERE object_type = 'PROCEDURE'
        ORDER BY object_name
    """)

    procedures = []
    for row in cursor.fetchall():
        nome = row[0]

        # busca o código fonte
        cursor2 = cursor.connection.cursor()
        cursor2.execute("""
            SELECT text
            FROM user_source
            WHERE name = :nome
              AND type = 'PROCEDURE'
            ORDER BY line
        """, nome=nome)

        codigo = "".join([l[0] for l in cursor2.fetchall()])
        cursor2.close()

        procedures.append({
            "nome": nome,
            "status": row[1],
            "ultima_alteracao": row[2],
            "codigo": codigo,
            "argumentos": extrairArgumentos(cursor, nome),
            "dependencias": extrairDependenciasProcedure(cursor, nome)
        })

    return procedures