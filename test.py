from flask import Flask, render_template, request, send_file
import os
import xlwings as xw
import tempfile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        f7_value = request.form['f7']
        f9_value = request.form['f9']
        f11_value = request.form['f11']
        f13_value = request.form['f13']
        f15_value = request.form['f15']

        # Open the workbook using xlwings
        wb = xw.Book(os.path.abspath('slabsr2.xlsx'))

        # Update the values in the worksheet
        wb.sheets['Sheet1'].range('F7').value = f7_value
        wb.sheets['Sheet1'].range('F9').value = f9_value
        wb.sheets['Sheet1'].range('F11').value = f11_value
        wb.sheets['Sheet1'].range('F13').value = f13_value
        wb.sheets['Sheet1'].range('F15').value = f15_value

        # Save the workbook
        wb.save()

        # Export the workbook to PDF
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            wb.api.ExportAsFixedFormat(0, tmp.name)
            tmp.flush()

        # Download the PDF file
        return send_file(tmp.name, as_attachment=True, attachment_filename='output.pdf')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
