import xlwings as xw

def std_editor():
    # Open the workbook
    # wb = xw.Book('oht.xlsm')
    app = xw.App(visible=False)
    wb = app.books.open('ohts.xlsm')
    wb.macro('stdeeditor')
    # app.api.Run('stdeeditor')
    # sheet = wb.sheets['std']
    # start = 22

    # noofcol = sheet.range('C2').value
    # stght = sheet.range('C3').value
    # noofbm = sheet.range('C4').value
    # fdndp = sheet.range('C5').value
    # colrd = sheet.range('C6').value
    # colsz = sheet.range('C7').value
    # tbwd = sheet.range('C8').value
    # tbdp = sheet.range('C9').value
    # bgwd = sheet.range('C10').value
    # bgdp = sheet.range('C11').value

    # noofjt = noofcol * (noofbm + 2) + 1

    # var1 = start + 8

    # # part1
    # sheet.range('A22').value = sheet.range('J3').value
    # sheet.range('A23').value = sheet.range('J4').value
    # sheet.range('A24').value = sheet.range('J5').value
    # sheet.range('A25').value = sheet.range('J6').value
    # sheet.range('A26').value = sheet.range('J7').value
    # sheet.range('A27').value = sheet.range('J8').value
    # sheet.range('A28').value = sheet.range('J9').value
    # sheet.range('A29').value = sheet.range('J10').value
    # sheet.range('A30').value = sheet.range('J11').value

    # # part2
    # for i in range(1, int(noofjt)):
    #     sheet.cells(var1 + i, 1).value = i
    #     sheet.cells(var1 + i, 2).value = colrd

    #     temp1 = int(i / noofcol - 0.05) + 1
    #     if temp1 == 1:
    #         sheet.cells(var1 + i, 3).value = -fdndp
    #     else:
    #         sheet.cells(var1 + i, 3).value = (temp1 - 2) * stght / noofbm
    #     sheet.cells(var1 + i, 4).value = (i - 1) / noofcol * 360
    #     sheet.cells(var1 + i, 5).value = ";"

    # sheet.cells(var1 + noofjt, 1).value = noofjt
    # sheet.cells(var1 + noofjt, 2).value = 0
    # sheet.cells(var1 + noofjt, 3).value = stght + sheet.range('F2').value
    # sheet.cells(var1 + noofjt, 4).value = 0
    # sheet.cells(var1 + noofjt, 5).value = ";"

    # # part3
    # sheet.cells(var1 + noofjt + 1, 1).value = sheet.range('J12').value
    # sheet.cells(var1 + noofjt + 2, 1).value = sheet.range('J13').value

    # i = noofjt + 3
    # noofcolmemb = (noofbm + 1) * noofcol
    # noofbmmemb = noofcol * (noofbm + 1)

    # for j in range(1, int(noofcolmemb) + 1):
    #     sheet.cells(var1 + i, 1).value = j
    #     i += 1

    # # Save and close the workbook
   
    import pandas as pd

    #     # Read Excel file
    df = pd.read_excel('ohts.xlsm', sheet_name='std')

        # Convert DataFrame to text
    text_data = df.to_string(index=False)

        # Write text data to a file
    with open('output.txt', 'w') as file:
        file.write(text_data)
    wb.save()
    wb.close()
std_editor()   