This reporter will run all the scripts in the /reportscripts folder, each of which can compile a report from data in the openbadger and CSOL databases.  Each report is then uploaded to a Google Spreadsheet specified in the config file.


```bash
python ./report.py
```

Sample config.py:

```bash
OPENBADGER_MONGO_HOST = 'blah.blug.com'
OPENBADGER_MONGO_PORT = 27017
OPENBADGER_MONGO_DB = 'bloateddb'
CSOL_MYSQL_HOST = 'otherblah.blug.com'
CSOL_MYSQL_PORT = 3306
CSOL_MYSQL_USER = 'ote'
CSOL_MYSQL_PASS = 'misterfunkyedogg'
CSOL_MYSQL_DB = 'fancydb'
CSOL_MYSQL_SSL_CA_PATH = 'securitystuff/mysql-ssl-ca-cert.pem'
GOOGLE_CLIENT_SECRETS_PATH = './client_secrets.json'
GOOGLE_REDIRECT_URI        = 'http://localhost:1234'
GOOGLE_SPREADSHEET_KEY     = 'HappyTimesThisIsASpreadsheetKey'
```