import statistics_by_property
import csv
import operator
from collections import defaultdict

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
  
  with open('./output/badges_by_issuer.csv', 'wb') as file:
    writer = csv.writer(file)
    writer.writerow(['Issuer', 'Number of Badges Issued'])
    
    for issuer, count in issuerCounts.iteritems():

      writer.writerow([issuer, count])
