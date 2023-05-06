from flask import Flask, request, send_file
import ezdxf

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get building parameters from the form
        length = float(request.form['length'])
        width = float(request.form['width'])
        height = float(request.form['height'])
        num_floors = int(request.form['num_floors'])

        # Generate DXF file
        doc = ezdxf.new(dxfversion='R2010')
        msp = doc.modelspace()

        # Create bottom floor
        x_min = -length/2
        x_max = length/2

        y_min = -width/2
        y_max = width/2
        msp.add_lwpolyline([(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max), (x_min, y_min)])

        # Create top floors and support columns
        for i in range(1, num_floors):
            z = i * height

            # Create floor
            msp.add_lwpolyline([(x_min, y_min, z), (x_max, y_min, z), (x_max, y_max, z), (x_min, y_max, z), (x_min, y_min, z)])

            # Create support columns
            col_radius = width / 10
            col_spacing = length / 2 - col_radius
            for j in range(4):
                x = length / 2 * (-1 if j == 0 else 1)
                y = width / 2 * (-1 if j == 1 or j == 2 else 1)
                msp.add_circle((x, y, z), col_radius)

        filename = 'building.dxf'
        doc.saveas(filename)

        # Download the file
        return send_file(filename, as_attachment=True)

    # Render the form
    return '''
        <form method="post">
            <label for="length">Length:</label>
            <input type="number" name="length" id="length" required><br><br>

            <label for="width">Width:</label>
            <input type="number" name="width" id="width" required><br><br>

            <label for="height">Height:</label>
            <input type="number" name="height" id="height" required><br><br>

            <label for="num_floors">Number of Floors:</label>
            <input type="number" name="num_floors" id="num_floors" required><br><br>

            <button type="submit">Generate DXF File</button>
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)