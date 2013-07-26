from report import Report
import helper_queries


def createReport(openbadgerDB, csolDB):
  badgesBySchool = helper_queries.getBadgesByProperty('school')
  learnersBySchool = helper_queries.getLearnersByProperty('school')
  activeLearnersBySchool = helper_queries.getLearnersByProperty('school', badgeThreshold=1)
  
  report = Report('Statistics by School', 4)
  
  schools = sorted(learnersBySchool.keys())
  
  for school in schools:
    report.addRow([school.title().decode('latin-1'), badgesBySchool[school], learnersBySchool[school], activeLearnersBySchool[school]])
  
  return report
