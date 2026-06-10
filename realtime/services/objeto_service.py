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

def carregarTabelas(cursor):
    return extrairTabelas(cursor)

def carregarViews(cursor):
    return extrairViews(cursor)

def carregarProcedures(cursor):
    return extrairProcedures(cursor)

def carregarFunctions(cursor):
    return extrairFunctions(cursor)

def carregarPackages(cursor):
    return extrairPackages(cursor)

def carregarTriggers(cursor):
    return extrairTriggers(cursor)

def carregarSequences(cursor):
    return extrairSequences(cursor)

def carregarIndexes(cursor):
    return extrairIndexes(cursor)

def carregarSynonyms(cursor):
    return extrairSynonyms(cursor)

def carregarJobs(cursor):
    return extrairJobs(cursor)
