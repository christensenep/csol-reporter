from report import Report
import helper_queries
import operator

def createReport(openbadgerDB, csolDB):
  learnersByZip = helper_queries.getLearnersByProperty('zipCode')

  report = Report('Top Zip Codes with Learners', 2)
  
  sortedLearnersByZip = sorted(learnersByZip.iteritems(), key=operator.itemgetter(1), reverse=True)
  
  for zip, count in sortedLearnersByZip:
    report.addRow([zip.title().decode('latin-1'), count])
  
  return report
