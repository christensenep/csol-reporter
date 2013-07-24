from pymongo import MongoClient
from os import listdir
import MySQLdb
import statistics_by_property
import config

_openbadgerDB = None
_csolDB = None

def init():
  global _openbadgerDB
  global _csolDB
  
  client = MongoClient(config.OPENBADGER_MONGO_HOST, config.OPENBADGER_MONGO_PORT)
  _openbadgerDB = client[config.OPENBADGER_MONGO_DB]

  _csolDB = MySQLdb.connect(host = config.CSOL_MYSQL_HOST,
                           port = config.CSOL_MYSQL_PORT,
                           user = config.CSOL_MYSQL_USER,
                           passwd = config.CSOL_MYSQL_PASS,
                           db = config.CSOL_MYSQL_DB,
                           ssl = {'ca' : config.CSOL_MYSQL_SSL_CA_PATH})
  
  statistics_by_property.init(_openbadgerDB, _csolDB)
  
def runScripts():
  moduleFiles = [name.split('.py')[0] for name in listdir('reportscripts') if name.endswith('.py')]
  for moduleFile in moduleFiles:
    script = __import__('reportscripts.' + moduleFile, fromlist=moduleFiles)
    if hasattr(script, 'createReport') and callable(getattr(script, 'createReport')):
      script.createReport(_openbadgerDB, _csolDB)

init()
runScripts()


