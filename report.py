class Report:

  def __init__(self, title, numCols):
    self.rows = []
    self.numCols = max(numCols,1)
    self.title = title

  def getTitle(self):
    return self.title
    
  def addRow(self, rowData):
    if type(rowData) is not list:
      newRow = [''] * self.numCols
      newRow[0] = rowData
    elif len(rowData) != self.numCols:
      newRow = []
      for i in range(self.numCols):
        if i < len(rowData):
          newRow.append(rowData[i])
        else:
          newRow.append('')
    else:
      newRow = rowData
      
    self.rows.append(newRow)
    
  def getRows(self):
    if len(self.rows) <= 0:
      return [[''] * self.numCols]
    else:
      return self.rows
    
  def getNumCols(self):
    return self.numCols
    
  def getNumRows(self):
    return len(self.rows) + 1
    
  