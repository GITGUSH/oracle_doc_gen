def extrairSynonyms(cursor):
    cursor.execute("""
        SELECT
            synonym_name,
            table_owner,
            table_name,
            db_link
        FROM user_synonyms
        ORDER BY synonym_name
    """)

    synonyms = []
    for row in cursor.fetchall():
        synonyms.append({
            "nome": row[0],
            "owner_referenciado": row[1],
            "objeto_referenciado": row[2],
            "db_link": row[3]
        })

    return synonyms