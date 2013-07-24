import statistics_by_property
import csv
import operator

def createReport(openbadgerDB, csolDB):
  badgesByZip = statistics_by_property.getBadgesByProperty('zipCode')
  learnersByZip = statistics_by_property.getLearnersByProperty('zipCode')
  activeLearnersByZip = statistics_by_property.getLearnersByProperty('zipCode', badgeThreshold=1)
  
  with open('./output/statistics_by_zip.csv', 'wb') as file:
    writer = csv.writer(file)
    writer.writerow(['Zip Code', 'Number of Badges Awarded', 'Number of Learners', 'Number of Learners With At Least One Badge'])

    for zip in learnersByZip:
      writer.writerow([zip, badgesByZip[zip], learnersByZip[zip], activeLearnersByZip[zip]])
