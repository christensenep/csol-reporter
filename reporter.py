import pymongo
import os
import MySQLdb
import helper_queries
import config
import oauth2client.client
import oauth2client.tools
import oauth2client.file
import gdata.spreadsheets.client
import gdata.spreadsheets.data
import gdata.gauth
import urlparse

_openbadgerDB = None
_csolDB = None
_worksheetDict = None
_spreadsheetClient = None

def init():
  global _openbadgerDB
  global _csolDB
  global _worksheetDict
  global _spreadsheetClient
  
  #openbadger mongo connection
  mongoClient = pymongo.MongoClient(config.OPENBADGER_MONGO_HOST, config.OPENBADGER_MONGO_PORT)
  _openbadgerDB = mongoClient[config.OPENBADGER_MONGO_DB]

  #csol mysql connection
  _csolDB = MySQLdb.connect(host = config.CSOL_MYSQL_HOST,
                           port = config.CSOL_MYSQL_PORT,
                           user = config.CSOL_MYSQL_USER,
                           passwd = config.CSOL_MYSQL_PASS,
                           db = config.CSOL_MYSQL_DB,
                           ssl = {'ca' : config.CSOL_MYSQL_SSL_CA_PATH})
  
  helper_queries.init(_openbadgerDB, _csolDB)
  
  #google api connection
  flow = oauth2client.client.flow_from_clientsecrets(config.GOOGLE_CLIENT_SECRETS_PATH,
                                                     scope = 'https://spreadsheets.google.com/feeds https://docs.google.com/feeds',
                                                     redirect_uri = config.GOOGLE_REDIRECT_URI)

  storage = oauth2client.file.Storage('credentials.dat')
  credentials = storage.get()
  
  if credentials is None or credentials.invalid:
    credentials = oauth2client.tools.run(flow, storage)

  token = gdata.gauth.OAuth2Token(client_id=credentials.client_id,
                                  client_secret=credentials.client_secret,
                                  scope='https://spreadsheets.google.com/feeds https://docs.google.com/feeds',
                                  user_agent=credentials.user_agent,
                                  access_token=credentials.access_token,
                                  refresh_token=credentials.refresh_token)
                                  
  _spreadsheetClient = gdata.spreadsheets.client.SpreadsheetsClient()
  token.authorize(_spreadsheetClient)
  
  worksheets = _spreadsheetClient.GetWorksheets(config.GOOGLE_SPREADSHEET_KEY)
  
  _worksheetDict = {}
  for worksheet in worksheets.entry:
    _worksheetDict[worksheet.title.text] = worksheet
  
def runScripts():
  moduleFiles = [name.split('.py')[0] for name in os.listdir('reportscripts') if name.endswith('.py')]
  for moduleFile in moduleFiles:
    script = __import__('reportscripts.' + moduleFile, fromlist=moduleFiles)
    if hasattr(script, 'createReport') and callable(getattr(script, 'createReport')):
      print 'Running ' + moduleFile
      report = script.createReport(_openbadgerDB, _csolDB)
      
      worksheet = None
      
      try:
        worksheet = _worksheetDict[report.getTitle()]
      except KeyError:
        print "Error - Couldn't find worksheet with title '" + report.getTitle() + "'"
      
      if worksheet:
        reportRows = report.getRows()
        
        worksheet.row_count.text = str(max(len(reportRows) + 1, 2))

        if len(reportRows) > 0:
          worksheet.col_count.text = str(len(reportRows[0]))
        
        _spreadsheetClient.Update(worksheet)
        
        batchUpdate = gdata.spreadsheets.data.BuildBatchCellsUpdate(config.GOOGLE_SPREADSHEET_KEY, worksheet.GetWorksheetId())

        rowNum = 2
        for row in reportRows:
          if rowNum % 1000 == 1:
            _spreadsheetClient.Batch(batchUpdate, force=True)
            batchUpdate = gdata.spreadsheets.data.BuildBatchCellsUpdate(config.GOOGLE_SPREADSHEET_KEY, worksheet.GetWorksheetId())
          colNum = 1
          for value in row:
            if isinstance( value, ( int, long ) ):
              value = str(value)
            batchUpdate.AddSetCell(rowNum, colNum, value)
            colNum += 1
          rowNum += 1
          
        _spreadsheetClient.Batch(batchUpdate, force=True)
  
init()
runScripts()


