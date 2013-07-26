from report import Report
from collections import defaultdict
import operator

def createReport(openbadgerDB, csolDB):
  
  issuerDocuments = openbadgerDB.issuers.find(None, {'name' : 1})

  issuerMap = defaultdict(str)
  for document in issuerDocuments:
    issuerMap[document['_id']] = document['name']

  programDocuments = openbadgerDB.programs.find(None, {'issuer': 1} )

  programMap = defaultdict(str)
  for document in programDocuments:
    programMap[document['_id']] = issuerMap[document['issuer']]

  badgeDocuments = openbadgerDB.badges.find(None, {'program' : 1})
 
  badgeMap = defaultdict(str)
  for document in badgeDocuments:
    badgeMap[document['_id']] = programMap[document['program']]
  
  badgeinstanceDocuments = openbadgerDB.badgeinstances.find(None, {'badge' : 1})
  
  issuerCounts = defaultdict(int)
  
  for document in badgeinstanceDocuments:
    issuerCounts[badgeMap[document['badge']]] += 1
  
  sortedIssuerCounts = sorted(issuerCounts.iteritems(), key=operator.itemgetter(1), reverse=True)
  
  report = Report('Top Badge Issuers', 2)
  
  for issuer, count in sortedIssuerCounts:
    report.addRow([issuer, count])
  
  return report

