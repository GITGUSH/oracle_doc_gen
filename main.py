import oracledb
import config
from extractor.tables import extrairTabelas


def conectar():
    conexao = oracledb.connect(
        user=config.USUARIO,
        password=config.SENHA,
        dsn=f"{config.HOST}:{config.PORTA}/{config.SERVICE}"
    )
    return conexao

#def testarConexao():
#    con = conectar()
#    cursor = con.cursor()
#    cursor.execute("SELECT 'Conexão Ok' FROM dual")
#    resultado = cursor.fetchone()
#    print(resultado[0])
#    cursor.close()
#    con.close()

#testarConexao()

def main():
    con = conectar()
    cursor = con.cursor()

    tabelas = extrairTabelas(cursor)

    print(f"Total de tabelas encontradas: {len(tabelas)}")
    for t in tabelas:
        print(f"-> {t['nome']} ({t['num_rows']} registros)")
        for col in t['colunas']:
            print(f"  {col['nome']} | {col['tipo']}({col['tamanho']}) | Nulável: {col['nulavel']}")
        print()

    cursor.close()
    con.close()

main()

