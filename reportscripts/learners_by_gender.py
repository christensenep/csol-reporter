from report import Report

def createReport(openbadgerDB, csolDB):
  cur = csolDB.cursor()

  queryString = ('SELECT '
                  'CASE '
                  '  WHEN gender = "male" THEN "Male" '
                  '  WHEN gender = "female" THEN "Female" '
                  '  ELSE "Not Specified" '
                  'END AS gender_readable, '
                  'COUNT(*) as count '
                  'FROM csol.Learners '
                  'GROUP BY gender '
                  'ORDER BY FIELD(gender_readable, "Female", "Male", "Not Specified");')
                
  cur.execute(queryString)

  report = Report('Learners by Gender', 2)
  
  for row in cur.fetchall():
    gender = row[0]
    count = row[1]

    if gender is None or gender == '':
      gender = 'Not Specified'

    report.addRow([gender.title(), count])

  return report
