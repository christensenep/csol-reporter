import statistics_by_property
import csv
import operator

def createReport(openbadgerDB, csolDB):
  cur = csolDB.cursor()

  queryString = ('SELECT LOWER(gender), COUNT(*) AS count '
                'FROM Learners '
                'GROUP BY gender')
                
  cur.execute(queryString)

  with open('./output/learners_by_gender.csv', 'wb') as file:
    writer = csv.writer(file)
    writer.writerow(['Gender', 'Number of Learners'])
    
    for row in cur.fetchall():
      gender = row[0]
      count = row[1]
	
      if gender is None or gender == '':
        gender = 'Not Specified'

      writer.writerow([gender.title(), count])
