

def extrairDependenciasView(cursor, nome_view):
    cursor.execute("""
        SELECT
            referenced_name,
            referenced_type
        FROM user_dependencies
        WHERE name = :view
          AND type = 'VIEW'
        ORDER BY referenced_name
    """, view=nome_view)

    dependencias = []
    for row in cursor.fetchall():
        dependencias.append({
            "nome": row[0],
            "tipo": row[1]
        })

    return dependencias


def extrairColunasView(cursor, nome_view):
    cursor.execute("""
        SELECT
            column_name,
            data_type,
            data_length,
            nullable
        FROM user_tab_columns
        WHERE table_name = :view
        ORDER BY column_id
    """, view=nome_view)

    colunas = []
    for row in cursor.fetchall():
        colunas.append({
            "nome": row[0],
            "tipo": row[1],
            "tamanho": row[2],
            "nulavel": "Sim" if row[3] == "Y" else "Não"
        })

    return colunas


def extrair_views(cursor):
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

        views.append({
            "nome": nome,
            "codigo": row[1],
            "colunas": colunas
        })

    return views


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
        views.append({
            "nome": nome,
            "codigo": row[1],
            "colunas": colunas,
            "dependencias": extrairDependenciasView(cursor, nome)
        })

    return views