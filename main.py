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
from generator.html.builder_functions import gerarFunctions
from generator.html.builder_packages import gerarPackages
from generator.html.builder_triggers import gerarTriggers
from generator.html.builder_sequences import gerarSequences
from generator.html.builder_indexes import gerarIndexes
from generator.html.builder_jobs import gerarJobs
from generator.html.builder_synonyms import gerarSynonyms

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
    print("1 - Gerar Documentação HTML")
    op = int(input("Informe a opção desejada: "))
    print()
    
    while op != 0:
        if op == 1:
            criarPastas(config.SCHEMA) #Cria a estrutura de pastas para o Schema
            copiarAssets()
            schema_data = mapearSchema(cursor, config.SCHEMA)
            gerarIndex(schema_data)
            gerarTabelas(schema_data)
            gerarViews(schema_data)
            gerarProcedures(schema_data)
            gerarFunctions(schema_data)
            gerarPackages(schema_data)
            gerarTriggers(schema_data)
            gerarSequences(schema_data)
            gerarIndexes(schema_data)
            gerarSynonyms(schema_data)
            gerarJobs(schema_data)
            break

        else:
            print("Opção inválida!")
            continue

    print("Encerrando Sistema...")        
    cursor.close()
    con.close()

main()

