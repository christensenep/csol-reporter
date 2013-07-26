from report import Report
import helper_queries
import operator

def createReport(openbadgerDB, csolDB):
  activeLearnersByZip = helper_queries.getLearnersByProperty('zipCode', badgeThreshold=1)

  report = Report('Top Zip Codes with Active Learners', 2)
  
  sortedActiveLearnersByZip = sorted(activeLearnersByZip.iteritems(), key=operator.itemgetter(1), reverse=True)
  
  for zip, count in sortedActiveLearnersByZip:
    report.addRow([zip.title().decode('latin-1'), count])
  
  return report
