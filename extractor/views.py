def extrairColunasView(cursor, nome_view):
    cursor2 = cursor.connection.cursor()
    cursor2.execute("""
        SELECT
            column_name,
            data_type,
            data_length,
            nullable
        FROM user_tab_columns
        WHERE table_name = :nome_view
        ORDER BY column_id
    """, nome_view=nome_view)

    colunas = []
    for row in cursor2.fetchall():
        colunas.append({
            "nome": row[0],
            "tipo": row[1],
            "tamanho": row[2],
            "nulavel": "Sim" if row[3] == "Y" else "Não"
        })

    cursor2.close()
    return colunas


def extrairDependenciasView(cursor, nome_view):
    cursor2 = cursor.connection.cursor()
    cursor2.execute("""
        SELECT
            referenced_name,
            referenced_type
        FROM user_dependencies
        WHERE name = :nome_view
          AND type = 'VIEW'
        ORDER BY referenced_name
    """, nome_view=nome_view)

    dependencias = []
    for row in cursor2.fetchall():
        dependencias.append({
            "nome": row[0],
            "tipo": row[1]
        })

    cursor2.close()
    return dependencias


def extrairViews(cursor):
    cursor.execute("""
        SELECT
            view_name,
            text
        FROM user_views
        ORDER BY view_name
    """)

    views = []
    for row in cursor.fetchall():
        nome = row[0]
        colunas = extrairColunasView(cursor, nome)
        dependencias = extrairDependenciasView(cursor, nome)

        views.append({
            "nome": nome,
            "codigo": row[1],
            "colunas": colunas,
            "dependencias": dependencias
        })

    return views