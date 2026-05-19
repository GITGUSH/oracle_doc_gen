import oracledb
import config
from extractor.tables import extrairTabela


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

    tabelas = extrairTabela(cursor)

    print(f"Total de tabelas encontradas: {len(tabelas)}")
    for t in tabelas:
        print(f"-> {t['nome']} ({t['num_rows']} registros)")

    cursor.close()
    con.close()

main()

