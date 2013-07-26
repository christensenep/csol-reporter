from report import Report
import helper_queries
from collections import defaultdict
import operator

def createReport(openbadgerDB, csolDB):

  issuerDocuments = openbadgerDB.issuers.find(None, {'name' : 1})

  issuerMap = defaultdict(str)
  for document in issuerDocuments:
    issuerMap[document['_id']] = document['name']

  programDocuments = openbadgerDB.programs.find(None, {'issuer': 1, 'name':1} )

  programMap = defaultdict(str)
  for document in programDocuments:
    programMap[document['_id']] = { 'name' : document['name'], 'issuer' : issuerMap[document['issuer']] }

  badgeDocuments = openbadgerDB.badges.find(None, {'name' : 1, 'program' : 1, 'categoryAward' : 1})
 
  badgeMap = defaultdict(str)
  for document in badgeDocuments:
    programInfo = programMap[document['program']]
    badgeMap[document['_id']] = { 'name' : document['name'], 
                                  'issuer' : programInfo['issuer'], 
                                  'program' : programInfo['name'], 
                                  'isSteam' : True if document['categoryAward'] != '' else False,
                                  'issuedCodes' : 0,
                                  'claimedReservedCodes' : 0,
                                  'claimedUnreservedCodes' : 0,
                                  'multiCodes' : 0,
                                  'reservedCodes' : 0,
                                  'unreservedCodes' : 0,
                                  'claimedCodes' : 0,
                                  'totalAwarded' : 0,
                                  'externallyAwarded' : 0,
                                  'steamAwards' : 0
                                }
  
  countsPerBadgePipeline =  [{'$project' : { 'claimCodes' : 1, '_id' : 1 } },
               { '$unwind' : '$claimCodes' } , 
               {'$project' : { 'claimCodes' : 1, 'claimed' : { '$and': '$claimCodes.claimedBy' }, 'reserved' : { '$and': '$claimCodes.reservedFor' }, 'multi' : { '$and' : '$claimCodes.multi' } } },
               { '$group' : { '_id' : '$_id', 
                              'issuedCodes' : { '$sum' : 1 }, 
                              'claimedReservedCodes' : { '$sum' : {'$cond' : [ { '$and' : ['$claimed', '$reserved'] }, 1, 0] } },  
                              'claimedUnreservedCodes' : { '$sum' : {'$cond' : [ { '$and' : ['$claimed', { '$not' : '$reserved' }, { '$not' : '$multi' } ] }, 1, 0] } }, 
                              'claimedCodes' : { '$sum' : {'$cond' : [ { '$and' : ['$claimed', { '$not' : '$multi' } ] }, 1, 0] } }, 
                              'reservedCodes' : { '$sum' : {'$cond' : ['$reserved', 1, 0] } }, 
                              'multiCodes' : { '$sum' : {'$cond' : ['$multi', 1, 0] } }, 
                            }
               }
              ]
              
  countsPerBadge = openbadgerDB.badges.aggregate(countsPerBadgePipeline)

  for row in countsPerBadge['result']:
    badge = badgeMap[row['_id']]
    issuedCodes = row['issuedCodes']
    reservedCodes = row['reservedCodes']
    multiCodes = row['multiCodes']
    
    badge['issuedCodes'] = issuedCodes
    badge['reservedCodes'] = reservedCodes
    badge['unreservedCodes'] = issuedCodes - reservedCodes - multiCodes
    badge['multiCodes'] = multiCodes
    badge['claimedCodes'] = row['claimedCodes']
    badge['claimedReservedCodes'] = row['claimedReservedCodes']
    badge['claimedUnreservedCodes'] = row['claimedUnreservedCodes']

  instancesPerBadgePipeline = [ 
                              {'$project' : { 'badge' : 1 } },
                              { '$group' : { '_id' : '$badge', 'count' : { '$sum' : 1 } } },
                             ]
               
  instancesPerBadge = openbadgerDB.badgeinstances.aggregate(instancesPerBadgePipeline)
  
  for row in instancesPerBadge['result']:
    badge = badgeMap[row['_id']]
    totalAwarded = row['count']
    badge['totalAwarded'] = totalAwarded
    badge['externallyAwarded'] = 0 if badge['isSteam'] else totalAwarded - badge['claimedCodes']
    badge['steamAwards'] = totalAwarded if badge['isSteam'] else 0
  
  sortedBadgeData = sorted(badgeMap.itervalues(), key=operator.itemgetter('issuer', 'program', 'name'))
  
  report = Report('Badge Data', 13)
  
  for badge in sortedBadgeData:
    if badge['totalAwarded'] != 0 or badge['issuedCodes'] != 0:
      report.addRow([badge['issuer'], badge['program'], badge['name'], badge['totalAwarded'], badge['issuedCodes'], badge['reservedCodes'], 
                     badge['unreservedCodes'], badge['multiCodes'], badge['claimedCodes'], badge['claimedReservedCodes'], badge['claimedUnreservedCodes'],
                     badge['externallyAwarded'], badge['steamAwards']])

  return report
  

