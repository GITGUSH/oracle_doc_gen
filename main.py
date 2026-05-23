import oracledb
import config
from extractor.tables import extrairTabelas
from extractor.views import extrairViews
from extractor.procedures import extrairProcedures
from extractor.functions import extrairFunctions


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
    
    print("MENU")
    print("0 - Sair")
    print("1 - Tabelas")
    print("2 - Views")
    print("3 - Procedures")
    print("4 - Functions")
    op = int(input("Informe a opção desejada: "))
    print()
    
    while op != 0:
        if op == 1:
            tabelas = extrairTabelas(cursor)
            print(f"Total de tabelas encontradas: {len(tabelas)}")
            for t in tabelas:
                print(f"-> {t['nome']} ({t['num_rows']} registros)")
                for col in t['colunas']:
                    print(f"  {col['nome']} | {col['tipo']}({col['tamanho']}) | Nulável: {col['nulavel']}")

                for c in t['constraints']:
                    if c['tipo'] == 'PK':
                        print(f"  [PK] {c['coluna']}")
                    else:
                        print(f"  [FK] {c['coluna']} → {c['tabela_ref']}")
                print()

        elif op == 2:
            views = extrairViews(cursor)
            print(f"Total de views: {len(views)}\n")
            for v in views:
                print(f"  → {v['nome']}")
                for col in v['colunas']:
                    print(f"    {col['nome']} | {col['tipo']}({col['tamanho']}) | Nulável: {col['nulavel']}")
                
                for dep in v['dependencias']:
                    print(f"    [DEP] {dep['nome']} ({dep['tipo']})")
                print()
            print()

        elif op == 3:
            procedures = extrairProcedures(cursor)
            print(f"Total de procedures: {len(procedures)}\n")
            for p in procedures:
                print(f"  → {p['nome']} | Status: {p['status']} | Alterado em: {p['ultima_alteracao']}")
                for arg in p['argumentos']:
                    print(f"    [{arg['direcao']}] {arg['nome']} | {arg['tipo']}")
        
                for dep in p['dependencias']:
                    print(f"    [DEP] {dep['nome']} ({dep['tipo']})")
                print()

        elif op == 4:
            functions = extrairFunctions(cursor)
            print(f"Total de functions: {len(functions)}\n")
            for f in functions:
                print(f"  → {f['nome']} | Status: {f['status']}")
                for arg in f['argumentos']:
                    print(f"    [{arg['direcao']}] {arg['nome']} | {arg['tipo']}")
                for dep in f[f"dependencias"]:
                    print(f"    [DEP] {dep['nome']} ({dep['tipo']})")
                print()


        print("MENU")
        print("0 - Sair")
        print("1 - Tabelas")
        print("2 - Views")
        print("3 - Procedures")
        print("4 - Functions")
        op = int(input("Informe a opção desejada: "))
        print()

    cursor.close()
    con.close()


main()

