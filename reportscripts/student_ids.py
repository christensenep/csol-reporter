from report import Report
import helper_queries
import operator

def createReport(openbadgerDB, csolDB):
  
  cur = csolDB.cursor()
  queryString = ("SELECT DISTINCT cpsStudentId FROM Learners "
                 "ORDER BY cpsStudentId ASC ")                
  cur.execute(queryString)
  
  report = Report('Student IDs', 1)
  
  for row in cur.fetchall():
    id = row[0]
    if id != '':
      report.addRow([id])
    
  return report
