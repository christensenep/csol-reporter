from report import Report

def createReport(openbadgerDB, csolDB):
  cur = csolDB.cursor()

  queryString = ("SELECT "
                 "CASE "
                 "WHEN age < 13 THEN 'Under 13' "
                 "WHEN age BETWEEN 13 AND 17 THEN '13-17' "
                 "WHEN age BETWEEN 18 AND 24 THEN '18-24' "
		              "WHEN age > 24 THEN 'Over 24' "
                  "END AS age_range, "
                  "COUNT(*) AS count "
                  "FROM (SELECT TIMESTAMPDIFF(YEAR, birthday, CURDATE()) AS age FROM csol.Learners) AS derived "
                  "GROUP BY age_range "
                  "ORDER BY FIELD(age_range, 'Under 13', '13-17', '18-24', 'Over 24'); ")
                
  cur.execute(queryString)

  report = Report('Learners by Age', 2)
  
  for row in cur.fetchall():
    age = row[0]
    count = row[1]
    
    report.addRow([age, count])
  
  return report
  