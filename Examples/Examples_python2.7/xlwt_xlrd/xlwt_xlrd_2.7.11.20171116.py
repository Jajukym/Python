#libraries
from xlwt import Workbook, Formula, easyxf #create a workbook
import xlwt #write to an existing workbook
import xlrd #read an existing workbook



#code read

a = xlrd.open_workbook("./EQF1259 App Procedures.xlsx") #open the created excel file

#print a.nsheets #number of sheets
#print a.sheet_names() #and their names

s = a.sheet_by_index(0) #select first sheet
t = a.sheet_by_index(1)
u = a.sheet_by_index(2)

#print s.nrows #number of rows used in a sheet
#print s.ncols #number of columbs used in a sheet

#print s.row_values(1) #row cell data
#print s.col_values(1) #column cell data


#b = s.cell(0,0).value
c = t.cell(1,1).value #get one cell value preferred method!!!
d = u.cell(1,1).value
#dt = xlrd.xdate_as_tuple(d,b.datemode) #convert a date in cell
#print b
print d
print c

#print sum(a) #and their sum
#print dt



#code create
wb = Workbook() #create a workbook
sheet1 = wb.add_sheet('Sheet1') #add sheets
#sheet2 = wb.add_sheet('Page 2')

sheet1.write(2,13, d + c) #writing to cells
#sheet1.write(1,13, 'The')
#sheet2.write(2,13, 'other words here')

#sheet1.col(13).width = 7000 #column width
#sheet2.col(13).width = 7000

#style2 = easyxf('pattern: pattern solid,fore_colour red;') #cell styling

#for i in xrange(10): #function of writing 1-10 in column 0 sheet2
    #sheet2.write(i,0,i)

#sheet2.write(10,0,Formula('SUM(A1:A10)'),style2) #adding column 0 and adding the style2

wb.save('Workbook Example.xls') #save created workbook
