from report import Report
import helper_queries
import operator

def createReport(openbadgerDB, csolDB):
  learnersBySchool = helper_queries.getLearnersByProperty('school')

  report = Report('Top Schools with Learners', 2)
  
  sortedLearnersBySchool = sorted(learnersBySchool.iteritems(), key=operator.itemgetter(1), reverse=True)
  
  for school, count in sortedLearnersBySchool:
    report.addRow([school.title().decode('latin-1'), count])
  
  return report
