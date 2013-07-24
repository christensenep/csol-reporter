import statistics_by_property
import csv
import operator

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

  countList = [0,0,0,0,0]
  
  for row in results:
    countList[row['_id']-1] = row['count']
  
  with open('./output/learners_by_steam_count.csv', 'wb') as file:
    writer = csv.writer(file)
    writer.writerow(['STEAM Badges Earned', 'Number of Learners'])
    
    for i in range(len(countList)):
      writer.writerow([i+1, countList[i]])
