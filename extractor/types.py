def extrairAtributosType(cursor, nome_type):
    cursor2 = cursor.connection.cursor()
    cursor2.execute("""
        SELECT
            attr_name,
            attr_type_name,
            length,
            precision,
            scale,
            attr_no
        FROM user_type_attrs
        WHERE type_name = :nome_type
        ORDER BY attr_no
    """, nome_type=nome_type)

    atributos = []
    for row in cursor2.fetchall():
        atributos.append({
            "nome": row[0],
            "tipo": row[1],
            "tamanho": row[2],
            "precisao": row[3],
            "escala": row[4],
            "ordem": row[5]
        })

    cursor2.close()
    return atributos


def extrairDependenciasType(cursor, nome_type):
    cursor2 = cursor.connection.cursor()
    cursor2.execute("""
        SELECT
            referenced_name,
            referenced_type
        FROM user_dependencies
        WHERE name = :nome_type
          AND type = 'TYPE'
        ORDER BY referenced_name
    """, nome_type=nome_type)

    dependencias = []
    for row in cursor2.fetchall():
        dependencias.append({
            "nome": row[0],
            "tipo": row[1]
        })

    cursor2.close()
    return dependencias


def extrairTypes(cursor):
    cursor.execute("""
        SELECT
            t.type_name,
            t.typecode,
            t.attributes,
            t.methods,
            o.status
        FROM user_types t
        JOIN user_objects o
            ON o.object_name = t.type_name
            AND o.object_type = 'TYPE'
        ORDER BY t.type_name
    """)

    types = []
    for row in cursor.fetchall():
        nome = row[0]

        types.append({
            "nome": nome,
            "typecode": row[1],
            "num_atributos": row[2],
            "num_metodos": row[3],
            "status": row[4],
            "atributos": extrairAtributosType(cursor, nome),
            "dependencias": extrairDependenciasType(cursor, nome)
        })

    return types