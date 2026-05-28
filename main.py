import oracledb
import config
from extractor.tables import extrairTabelas
from extractor.views import extrairViews
from extractor.procedures import extrairProcedures
from extractor.functions import extrairFunctions
from extractor.packages import extrairPackages
from extractor.triggers import extrairTriggers
from extractor.types import extrairTypes
from extractor.indexes import extrairIndexes
from extractor.sequences import extrairSequences
from extractor.synonyms import extrairSynonyms
from extractor.jobs import extrairJobs
from extractor.dependencies import extrairDependencies, agruparDependencias
from processor.schema_map import mapearSchema
from generator.html.builder import criarPastas, copiarAssets
from generator.html.index import gerarIndex
from generator.html.builder_tables import gerarTabelas
from generator.html.builder_views import gerarViews
from generator.html.builder_procedures import gerarProcedures

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
    print("5 - Packages")
    print("6 - Triggers")
    print("7 - Types")
    print("8 - Indexes")
    print("9 - Sequences")
    print("10 - Synonyms")
    print("11 - Jobs")
    print("12 - Dependências") 
    print("13 - Mapear schema completo") 
    print("14 - Resumo das relações entre tabelas")
    print("15 - Resumo do grafo de dependências")
    print("16 - Preparar estrutura para geração de documentação HTML")
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
        
        elif op == 5:
            packages = extrairPackages(cursor)
            print(f"Total de packages: {len(packages)}\n")
            for p in packages:
                print(f"  → {p['nome']} | Status: {p['status']}")
                for sub in p['subprogramas']:
                    print(f"    [SUB] {sub['nome']}")
                    for arg in sub['argumentos']:
                        print(f"      [{arg['direcao']}] {arg['nome']} | {arg['tipo']}")
                for dep in p['dependencias']:
                    print(f"    [DEP] {dep['nome']} ({dep['tipo']})")
                print()
                
        elif op == 6:
            triggers = extrairTriggers(cursor)
            print(f"Total de triggers: {len(triggers)}\n")
            for t in triggers:
                print(f"  → {t['nome']} | {t['tipo']} | Evento: {t['evento']} | Tabela: {t['tabela']} | Status: {t['status']}")
                for dep in t['dependencias']:
                    print(f"    [DEP] {dep['nome']} ({dep['tipo']})")
                print()
        
        elif op == 7:
            types = extrairTypes(cursor)
            print(f"Total de types: {len(types)}\n")
            for t in types:
                print(f"  → {t['nome']} | Typecode: {t['typecode']} | Status: {t['status']}")
                for atr in t['atributos']:
                    print(f"    {atr['nome']} | {atr['tipo']} | Ordem: {atr['ordem']}")
                for dep in t['dependencias']:
                    print(f"    [DEP] {dep['nome']} ({dep['tipo']})")
            print()
        
        elif op == 7:
            types = extrairTypes(cursor)
            print(f"Total de types: {len(types)}\n")
            for t in types:
                print(f"  → {t['nome']} | Typecode: {t['typecode']} | Status: {t['status']}")
                for atr in t['atributos']:
                    print(f"    {atr['nome']} | {atr['tipo']} | Ordem: {atr['ordem']}")
                for dep in t['dependencias']:
                    print(f"    [DEP] {dep['nome']} ({dep['tipo']})")
                print()
        
        elif op == 8:
            indexes = extrairIndexes(cursor)
            print(f"Total de indexes: {len(indexes)}\n")
            for i in indexes:
                print(f"  → {i['nome']} | Tabela: {i['tabela']} | Tipo: {i['tipo']} | Único: {i['unico']} | Status: {i['status']}")

                for col in i['colunas']:
                    print(f"    {col['nome']} | Posição: {col['posicao']} | Ordem: {col['ordem']}")   
                print()

        elif op == 9:
            sequences = extrairSequences(cursor)
            print(f"Total de sequences: {len(sequences)}\n")
            for s in sequences:
                print(f"  → {s['nome']} | Incremento: {s['incremento']} | Último valor: {s['ultimo_valor']} | Cíclico: {s['ciclico']}")
                print()
        
        elif op == 10:
            synonyms = extrairSynonyms(cursor)
            print(f"Total de synonyms: {len(synonyms)}\n")
            for s in synonyms:
                print(f"  → {s['nome']} | Aponta para: {s['owner_referenciado']}.{s['objeto_referenciado']}", end="")
                if s['db_link']:
                    print(f" | DB Link: {s['db_link']}", end="")
                print()

        elif op == 11:
            jobs = extrairJobs(cursor)
            print(f"Total de jobs: {len(jobs)}\n")
            for j in jobs:
                print(f"  → {j['nome']} | Tipo: {j['tipo']} | Estado: {j['estado']} | Habilitado: {j['habilitado']}")
                print(f"    Intervalo: {j['intervalo']}")
                print(f"    Última execução: {j['ultima_execucao']} | Próxima: {j['proxima_execucao']}")
                print(f"    Execuções: {j['qtd_execucoes']} | Falhas: {j['qtd_falhas']}")
                print()

        elif op == 12:
            dependencias = extrairDependencies(cursor)
            grafo = agruparDependencias(dependencias)

            print(f"Total de objetos com dependências: {len(grafo)}\n")
            for nome, info in grafo.items():
                print(f"  → {nome} ({info['tipo']})")
                for dep in info['depende_de']:
                    print(f"    depende de: {dep['owner']}.{dep['nome']} ({dep['tipo']})")
                print()
        
        elif op == 13:
            print(f"\nMapeando schema {config.SCHEMA}...\n")
            schema = mapearSchema(cursor, config.SCHEMA)

            print(f"\nResumo do schema {schema['schema']}:")
            print(f"  Tabelas:    {len(schema['tabelas'])}")
            print(f"  Views:      {len(schema['views'])}")
            print(f"  Sequences:  {len(schema['sequences'])}")
            print(f"  Procedures: {len(schema['procedures'])}")
            print(f"  Functions:  {len(schema['functions'])}")
            print(f"  Packages:   {len(schema['packages'])}")
            print(f"  Triggers:   {len(schema['triggers'])}")
            print(f"  Types:      {len(schema['types'])}")
            print(f"  Indexes:    {len(schema['indexes'])}")
            print(f"  Synonyms:   {len(schema['synonyms'])}")
            print(f"  Jobs:       {len(schema['jobs'])}")
            print()
        
        elif op == 14:
            schema = mapearSchema(cursor, config.SCHEMA)
            relacoes = schema["relacoes"]

            print(f"Total de relações encontradas: {len(relacoes)}\n")
            for r in relacoes:
                print(f"  {r['tabela_origem']}.{r['coluna_origem']} → {r['tabela_destino']}")
                print()

        elif op == 15:
            schema = mapearSchema(cursor, config.SCHEMA)
            from processor.deps_graph import resumoGrafo
            resumoGrafo(schema["grafo_deps"])

        elif op == 16:
            criarPastas(config.SCHEMA) #Cria a estrutura de pastas para o Schema
            copiarAssets()

            schema_data = mapearSchema(cursor, config.SCHEMA)

            gerarIndex(schema_data)

            gerarTabelas(schema_data)

            gerarViews(schema_data)

            gerarProcedures(schema_data)

        print()
        print("MENU")
        print("0 - Sair")
        print("1 - Tabelas")
        print("2 - Views")
        print("3 - Procedures")
        print("4 - Functions")
        print("5 - Packages")
        print("6 - Triggers")
        print("7 - Types")
        print("8 - Indexes")
        print("9 - Sequences")
        print("10 - Synonyms")
        print("11 - Jobs")
        print("12 - Dependências")
        print("13 - Mapear schema completo")
        print("14 - Resumo das relações entre tabelas")
        print("15 - Resumo do grafo de dependências")
        print("16 - Preparar estrutura para geração de documentação HTML")
        op = int(input("Informe a opção desejada: "))
        print()

    cursor.close()
    con.close()


main()

