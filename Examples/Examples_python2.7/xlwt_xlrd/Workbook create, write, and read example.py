#libraries
from xlwt import Workbook, Formula, easyxf #create a workbook
import xlwt #write to an existing workbook
import xlrd #read an existing workbook

#code create
wb = Workbook() #create a workbook
sheet1 = wb.add_sheet('Page 1') #add sheets
sheet2 = wb.add_sheet('Page 2')

sheet1.write(2,13, 'words here') #writing to cells
sheet1.write(1,13, 'The')
sheet2.write(2,13, 'other words here')

sheet1.col(13).width = 7000 #column width
sheet2.col(13).width = 7000

style2 = easyxf('pattern: pattern solid,fore_colour red;') #cell styling

for i in xrange(10): #function of writing 1-10 in column 0 sheet2
    sheet2.write(i,0,i)

sheet2.write(10,0,Formula('SUM(A1:A10)'),style2) #adding column 0 and adding the style2

wb.save('Workbook Example.xls') #save created workbook

#code read

b = xlrd.open_workbook("./Workbook Example.xls") #open the created excel file

print b.nsheets #number of sheets
print b.sheet_names() #and their names

s = b.sheet_by_index(0) #select first sheet

print s.nrows #number of rows used in a sheet
print s.ncols #number of columbs used in a sheet

print s.row_values(2) #row cell data
print s.col_values(13) #column cell data

a = s.col_values(13,2,3) #one cell at a time requires cell previous
d = s.cell(2,13).value #get one cell value preferred method!!!
#dt = xlrd.xdate_as_tuple(d,b.datemode) #convert a date in cell
print a
print d

#print sum(a) #and their sum
#print dt

