import xlsxwriter

def saveToExcel(filename, sheet, source, MostCommon40, freqDist):
    workbook = xlsxwriter.Workbook('filename')
    worksheet = workbook.add_worksheet()

    #worksheet.set_column('A:A', 40)

    worksheet.write('A1', source)
    worksheet.write('A2', MostCommon40)
    worksheet.write('A3', freqDist)

    workbook.close()
