from flask import Flask, render_template, request, send_file
import xlwings as xw

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        f7_value = request.form['f7']
        f9_value = request.form['f9']
        f11_value = request.form['f11']
        f13_value = request.form['f13']
        f15_value = request.form['f15']

        wb = xw.Book('slabsr2.xlsx')
        sht = wb.sheets.active

        sht.range('F7').value = f7_value
        sht.range('F9').value = f9_value
        sht.range('F11').value = f11_value
        sht.range('F13').value = f13_value
        sht.range('F15').value = f15_value

        wb.save('slabsr2.xlsx')
        wb.to_pdf('slabsr2.pdf')

        return send_file('slabsr2.pdf', as_attachment=True)

    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
