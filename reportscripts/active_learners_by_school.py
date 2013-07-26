from report import Report
import helper_queries
import operator

def createReport(openbadgerDB, csolDB):
  activeLearnersBySchool = helper_queries.getLearnersByProperty('school', badgeThreshold=1)

  report = Report('Top Schools with Active Learners', 2)
  
  sortedActiveLearnersBySchool = sorted(activeLearnersBySchool.iteritems(), key=operator.itemgetter(1), reverse=True)
  
  for school, count in sortedActiveLearnersBySchool:
    report.addRow([school.title().decode('latin-1'), count])
  
  return report
