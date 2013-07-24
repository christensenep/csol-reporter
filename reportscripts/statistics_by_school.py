import statistics_by_property
import csv
import operator

def createReport(openbadgerDB, csolDB):
  badgesBySchool = statistics_by_property.getBadgesByProperty('school')
  learnersBySchool = statistics_by_property.getLearnersByProperty('school')
  activeLearnersBySchool = statistics_by_property.getLearnersByProperty('school', badgeThreshold=1)
  
  with open('./output/statistics_by_school.csv', 'wb') as file:
    writer = csv.writer(file)
    writer.writerow(['School', 'Number of Badges Awarded', 'Number of Learners', 'Number of Learners With At Least One Badge'])
    
    for school in learnersBySchool:
      writer.writerow([school.title(), badgesBySchool[school], learnersBySchool[school], activeLearnersBySchool[school]])
