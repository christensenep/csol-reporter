from report import Report

def createReport(openbadgerDB, csolDB):
  badges = openbadgerDB.badges
  
  steamBadgeDocuments = openbadgerDB.badges.find( {'categoryAward' : { '$nin': ['', None] } }, fields=['_id']);
  steamBadges = []
  for document in steamBadgeDocuments:
    steamBadges.append(document['_id'])
  
  badgeinstances = openbadgerDB.badgeinstances

  pipeline = [{'$match' : {'badge' : { '$in' : steamBadges } } },
              {'$group' : {'_id' : '$user', 'count' : {'$sum' : 1}}},
              {'$group' : {'_id' : '$count', 'count' : {'$sum' : 1}}}]
              
  results = badgeinstances.aggregate(pipeline)['result']

  report = Report('Learners by STEAM Badges Earned', 2)
  
  countList = [0,0,0,0,0]
  
  for row in results:
    countList[row['_id']-1] = row['count']
  
  for i in range(len(countList)):
    report.addRow([i+1, countList[i]])

  return report
  
