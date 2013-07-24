from pymongo import MongoClient
from collections import defaultdict
import MySQLdb

_badgesByLearner = defaultdict(int)
_openbadgerDB = None
_csolDB = None

def init(openbadgerDB, csolDB):
  global _openbadgerDB
  global _csolDB
  global _badgesByLearner
  
  _openbadgerDB = openbadgerDB
  _csolDB = csolDB
  
  badgeinstances = _openbadgerDB.badgeinstances

  pipeline = [{'$group' : {'_id' : '$user', 'count' : {'$sum' : 1}}},
              {'$project' : {'email' : '$_id', 'count' : 1, '_id' : 0}}]
              
  results = badgeinstances.aggregate(pipeline)['result']

  for row in results:
    email = row['email']
    _badgesByLearner[email] = row['count']

def getLearnersByProperty(dbField, nullName='None Specified', badgeThreshold=0):
  cur = _csolDB.cursor()

  qualifyingEmails = []
  whereClause = ''

  if badgeThreshold > 0:
    for email, count in _badgesByLearner.iteritems():
      if count >= badgeThreshold:
        qualifyingEmails.append(email)
    
    formatString = ','.join(['%s'] * len(qualifyingEmails))
    whereClause = "WHERE email IN (%s)" % formatString
  
  queryString = ('SELECT LOWER(' + dbField + '), COUNT(*) AS count '
                'FROM Learners '
                + whereClause +
                'GROUP BY ' + dbField + ' ' 
                'ORDER BY count DESC ')
                
  cur.execute(queryString, tuple(qualifyingEmails))

  learnersByProperty = defaultdict(int)

  for row in cur.fetchall() :
    propertyValue = row[0]
    count = row[1]
    
    if propertyValue is None or propertyValue == '':
      propertyValue = nullName

    learnersByProperty[propertyValue] += count
    
  return learnersByProperty
  
    
def getBadgesByProperty(dbField, nullName='None Specified'):
  cur = _csolDB.cursor()

  cur.execute('SELECT email, LOWER(' + dbField + ') FROM csol.Learners')

  badgesByProperty = defaultdict(int)

  for row in cur.fetchall() :
    email = row[0]
    propertyValue = row[1]
    
    if propertyValue is None or propertyValue == '':
      propertyValue = nullName
    
    badgesByProperty[propertyValue] += _badgesByLearner[email]
    
  return badgesByProperty

  
  
