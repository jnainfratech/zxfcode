from flask import Flask, render_template, request, send_file
import xlwings as xw

app = Flask(__name__)

# Define the lists
List1 = [0,8,8,8,8,10,8,10,8,10,12,10,8,10,12,8,12,10,12,10,12,16,12,10,16,16,12,16,10,20,12,16,20,16,20,12,20,16,25,20,25,16,20,25,25,20,16,25,20,25,25,20,25,25]
List2 = [0,300,250,225,200,300,175,250,150,225,300,200,125,175,250,100,225,150,200,125,175,300,150,100,250,225,125,200,75,300,100,175,250,150,225,75,200,125,300,175,250,100,150,225,200,125,75,175,100,150,125,75,100,75]
List3 = [0,1.67,2,2.23,2.51,2.61,2.87,3.14,3.34,3.48,3.76,3.92,4.01,4.48,4.52,5.02,5.02,5.23,5.65,6.28,6.45,6.69,7.53,7.85,8.03,8.93,9.04,10.04,10.46,10.46,11.3,11.48,12.56,13.39,13.95,15.07,15.7,16.07,16.35,17.94,19.62,20.09,20.93,21.8,24.53,25.12,26.79,28.03,31.4,32.7,39.25,41.86,49.06,65.41]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the form values
        f7_value = request.form['f7']
        f9_value = request.form['f9']
        f11_value = request.form['f11']
        f13_value = request.form['f13']
        f15_value = request.form['f15']

        # Open the Excel workbook and select the active sheet
        wb = xw.Book('slabsr2.xlsx')
        sht = wb.sheets.active

        # Update the cell values
        sht.range('F7').value = f7_value
        sht.range('F9').value = f9_value
        sht.range('F11').value = f11_value
        sht.range('F13').value = f13_value
        sht.range('F15').value = f15_value

        # Update C66 and D66 based on List3 values
        for i in range(len(List1)):
            if List3[i] > sht.range('F60').value:
                sht.range('C66').value = List1[i]
                sht.range('D66').value = List2[i]
                wb.save()
                break

        # Update C67 and D67 based on List3 values
        for i in range(len(List1)):
            if List3[i] > sht.range('F61').value:
                sht.range('C67').value = List1[i]
                sht.range('D67').value = List2[i]
                wb.save()
                break

        # Update C68 and D68 based on List3 values
        for i in range(len(List1)):
            if List3[i] > sht.range('F62').value:
                sht.range('C68').value = List1[i]
                sht.range('D68').value = List2[i]
                wb.save()
                break

        # Update C69 and D69 based on List3 values
        for i in range(len(List1)):
            if List3[i] > sht.range('F63').value:
                sht.range('C69').value = List1[i]
                sht.range('D69').value = List2[i]
                wb.save()
                break

        # Save the workbook and convert it to PDF
        wb.save('slabsr2.xlsx')
        wb.to_pdf('slabsr2.pdf')

        # Return the PDF file as an attachment
        return send_file('slabsr2.pdf', as_attachment=True)

    else:
        # Render the HTML template if the request method is GET
        return render_template('index.html')

if __name__ == '__main__':
    app.run()