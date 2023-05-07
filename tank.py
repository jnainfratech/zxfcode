from flask import Flask, render_template, request, send_file
import xlwings as xw
import ezdxf
import zipfile
import math

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the form values
        radius_circle = float(request.form['radius_circle'])
        thickness = float(request.form['thickness'])
        no_of_rods = int(request.form['no_of_rods'])
        radius_rods = float(request.form['radius_rods'])
        
        # Generate the DXF file
        doc = ezdxf.readfile('arcdome.dxf') 
        msp = doc.modelspace()

        center = (0 , 0)
        thickness_radius =  (thickness+radius_circle)
        msp.add_circle(center, thickness_radius)

        center = (0 , 0)
        radius_middle = (radius_circle+ thickness/2)
        msp.add_circle(center, radius_middle) 
        

        center = (0 , 0)
        radius_circle = radius_circle
        circle = msp.add_circle(center, radius_circle, dxfattribs={'linetype': 'HIDDEN', 'ltscale': 100})
        circle.dxf.lineweight = 100
        circle.dxf.color = 4  

        # Number of circles to add
        n = no_of_rods

        # Radius of the small circles
        radius_small = radius_rods

        # Calculate the angle between each circle
        angle = 2 * math.pi / n

        # Add the small circles
        for i in range(n):
            # Calculate the center of the small circle
            x = center[0] + radius_middle * math.cos(i * angle)
            y = center[1] + radius_middle * math.sin(i * angle)
            center_small = (x, y)
            msp.add_circle(center_small, radius_small)
    
       # Save the DXF file
        filename = 'slab.dxf'
        doc.saveas(filename)

        # Download the file
        return send_file(filename, as_attachment=True)

    else:
        # Render the HTML template if the request method is GET
        return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True)