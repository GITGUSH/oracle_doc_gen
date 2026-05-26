from extractor.tables import extrairTabelas
from extractor.views import extrairViews
from extractor.sequences import extrairSequences
from extractor.procedures import extrairProcedures
from extractor.functions import extrairFunctions
from extractor.packages import extrairPackages
from extractor.triggers import extrairTriggers
from extractor.types import extrairTypes
from extractor.indexes import extrairIndexes
from extractor.synonyms import extrairSynonyms
from extractor.jobs import extrairJobs
from extractor.dependencies import extrairDependencies, agruparDependencias

def mapearSchema(cursor, schema):
    print("Extraindo tabelas...")
    tabelas = extrairTabelas(cursor)

    print("Extraindo views...")
    views = extrairViews(cursor)

    print("Extraindo sequences...")
    sequences = extrairSequences(cursor)

    print("Extraindo procedures...")
    procedures = extrairProcedures(cursor)

    print("Extraindo functions...")
    functions = extrairFunctions(cursor)

    print("Extraindo packages...")
    packages = extrairPackages(cursor)

    print("Extraindo triggers...")
    triggers = extrairTriggers(cursor)

    print("Extraindo types...")
    types = extrairTypes(cursor)

    print("Extraindo indexes...")
    indexes = extrairIndexes(cursor)

    print("Extraindo synonyms...")
    synonyms = extrairSynonyms(cursor)

    print("Extraindo jobs...")
    jobs = extrairJobs(cursor)

    print("Extraindo dependências...")
    dependencias = extrairDependencies(cursor)
    grafo = agruparDependencias(dependencias)

    return {
        "schema": schema,
        "tabelas": tabelas,
        "views": views,
        "sequences": sequences,
        "procedures": procedures,
        "functions": functions,
        "packages": packages,
        "triggers": triggers,
        "types": types,
        "indexes": indexes,
        "synonyms": synonyms,
        "jobs": jobs,
        "dependencias": grafo
    }