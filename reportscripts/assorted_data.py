from report import Report

def createReport(openbadgerDB, csolDB):
  cur = csolDB.cursor()
  
  report = Report('Other Data', 2)
  
  queryString = ("SELECT COUNT(*) FROM Learners")                
  cur.execute(queryString)
  learnerCount = cur.fetchone()[0]
  report.addRow(['Number of Learners', learnerCount])
  
  badgeInstanceCount = openbadgerDB.badgeinstances.count()
  report.addRow(['Number of Badges Awarded', badgeInstanceCount])
  
  steamBadgeDocuments = openbadgerDB.badges.find( {'categoryAward' : { '$nin': ['', None] } }, fields=['_id']);
  steamBadges = []
  for document in steamBadgeDocuments:
    steamBadges.append(document['_id'])
  steamBadgeInstances = openbadgerDB.badgeinstances.aggregate([{'$match' : {'badge' : { '$in' : steamBadges } } }] )
  steamBadgeInstanceCount = len(steamBadgeInstances['result'])
  report.addRow(['Number of STEAM Badges Awarded', steamBadgeInstanceCount])
  
  queryString = ("SELECT COUNT(*) FROM Playlists")
  cur.execute(queryString)
  wishlistCount = cur.fetchone()[0]
  report.addRow(['Number of Badges Wishlisted', wishlistCount])
 
  return report

