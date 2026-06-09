def extrairArgumentosPackage(cursor, nome_package, nome_subprograma):
    cursor.execute("""
        SELECT
            argument_name,
            data_type,
            in_out,
            position
        FROM user_arguments
        WHERE package_name = :package
          AND object_name = :subprograma
        ORDER BY position
    """, package=nome_package, subprograma=nome_subprograma)

    argumentos = []
    for row in cursor.fetchall():
        argumentos.append({
            "nome": row[0],
            "tipo": row[1],
            "direcao": row[2],
            "posicao": row[3]
        })

    return argumentos


def extrairSubprogramas(cursor, nome_package):
    cursor.execute("""
        SELECT DISTINCT
            object_name,
            procedure_name
        FROM user_procedures
        WHERE object_name = :package
          AND procedure_name IS NOT NULL
        ORDER BY procedure_name
    """, package=nome_package)

    subprogramas = []
    for row in cursor.fetchall():
        nome_sub = row[1]
        argumentos = extrairArgumentosPackage(cursor, nome_package, nome_sub)

        subprogramas.append({
            "nome": nome_sub,
            "argumentos": argumentos
        })

    return subprogramas


def extrairCodigoPackage(cursor, nome_package, tipo):
    cursor.execute("""
        SELECT text
        FROM user_source
        WHERE name = :nome
          AND type = :tipo
        ORDER BY line
    """, nome=nome_package, tipo=tipo)

    return "".join([l[0] for l in cursor.fetchall()])


def extrairDependenciasPackage(cursor, nome_package):
    cursor.execute("""
        SELECT
            referenced_name,
            referenced_type
        FROM user_dependencies
        WHERE name = :nome
          AND type = 'PACKAGE BODY'
        ORDER BY referenced_name
    """, nome=nome_package)

    dependencias = []
    for row in cursor.fetchall():
        dependencias.append({
            "nome": row[0],
            "tipo": row[1]
        })

    return dependencias


def extrairPackages(cursor):
    cursor.execute("""
        SELECT
            object_name,
            status,
            last_ddl_time
        FROM user_objects
        WHERE object_type = 'PACKAGE'
        ORDER BY object_name
    """)

    packages = []
    for row in cursor.fetchall():
        nome = row[0]

        packages.append({
            "nome": nome,
            "status": row[1],
            "ultima_alteracao": row[2],
            "header": extrairCodigoPackage(cursor, nome, 'PACKAGE'),
            "body": extrairCodigoPackage(cursor, nome, 'PACKAGE BODY'),
            "subprogramas": extrairSubprogramas(cursor, nome),
            "dependencias": extrairDependenciasPackage(cursor, nome)
        })

    return packages