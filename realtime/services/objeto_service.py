from extractor.tables import extrairTabelas
from extractor.views import extrairViews
from extractor.procedures import extrairProcedures
from extractor.functions import extrairFunctions
from extractor.packages import extrairPackages
from extractor.triggers import extrairTriggers
from extractor.sequences import extrairSequences
from extractor.indexes import extrairIndexes
from extractor.synonyms import extrairSynonyms
from extractor.jobs import extrairJobs

def carregarObjetos(cursor):
    return {
        "tabelas": extrairTabelas(cursor),
        "views": extrairViews(cursor),
        "procedures": extrairProcedures(cursor),
        "functions": extrairFunctions(cursor),
        "packages": extrairPackages(cursor),
        "triggers": extrairTriggers(cursor),
        "sequences": extrairSequences(cursor),
        "indexes": extrairIndexes(cursor),
        "synonyms": extrairSynonyms(cursor),
        "jobs": extrairJobs(cursor),
    }