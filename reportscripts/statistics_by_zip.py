from report import Report
import helper_queries


def createReport(openbadgerDB, csolDB):
  badgesByZip = helper_queries.getBadgesByProperty('zipCode')
  learnersByZip = helper_queries.getLearnersByProperty('zipCode')
  activeLearnersByZip = helper_queries.getLearnersByProperty('zipCode', badgeThreshold=1)
  
  report = Report('Statistics by Zip', 4)
  
  zips = sorted(learnersByZip.keys())
    
  for zip in zips:
    report.addRow([zip, badgesByZip[zip], learnersByZip[zip], activeLearnersByZip[zip]])
  
  return report
  

