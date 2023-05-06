from flask import Flask, render_template, request
from openpyxl import load_workbook

app = Flask(__name__)
book = load_workbook('slabsr2.xlsx')
sheet = book.active

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        f7_value = request.form['f7']
        f9_value = request.form['f9']
        f11_value = request.form['f11']
        f13_value = request.form['f13']
        f15_value = request.form['f15']

        sheet['F7'].value = f7_value
        sheet['F9'].value = f9_value
        sheet['F11'].value = f11_value
        sheet['F13'].value = f13_value
        sheet['F15'].value = f15_value

        book.save('slabsr2.xlsx')
        return 'Values updated successfully!'
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
