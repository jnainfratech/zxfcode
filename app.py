from flask import Flask, request, send_file
from PyNite import FEModel3D
import ezdxf
import math
import PyNite
from ezdxf.math import Vec2
import numpy as np
import matplotlib.pyplot as plt
import xlwings as xw
def nearest_multiple(x, y):
    quotient = x // y
    lower_multiple = y * quotient
    upper_multiple = y * (quotient + 1)
    
    if abs(x - lower_multiple) <= abs(x - upper_multiple):
        return lower_multiple
    else:
        return upper_multiple
def pmm_interaction_curve(fc, fy, b, d, moments):
    # Constants
    eps_c = 0.0035  # Strain at the extreme concrete fiber
    eps_y = fy / (200000 * np.sqrt(3))  # Strain at yield of steel
    eps_su = 0.0035 + (0.0035 * fy) / (0.87 * fc)  # Ultimate concrete strain

    # Calculate neutral axis depth
    #x = np.linspace(0, d,100)
    x = 0.2*d
    print("what is x",x)
    print("What is d",d)
    strain_comp = np.minimum(eps_su, x / d * eps_su)
    strain_steel = (d - x) / d * eps_c + x / d * eps_y
    strain_total = strain_comp + strain_steel

    # Calculate curvature
    curvature = strain_steel / (d - x)

    # Calculate moment capacity
    moment_capacity = b * d**2 * fc * (0.5 * (1 - eps_c / eps_su) * (d - eps_c / (2 * curvature)) - eps_c / (3 * curvature))

    # Plot interaction curve
    # plt.figure(figsize=(10, 6))
    # plt.plot(moment_capacity, -moments, label='Interaction Curve')
    # plt.scatter(moment_capacity, -moments, c='r', label='Points')
    # plt.xlabel('Moment Capacity (kNm)')
    # plt.ylabel('Axial Force (kN)')
    # plt.title('P-M-M Interaction Curve')
    # plt.grid(True)
    # plt.legend()

    # Calculate required area of steel for a given moment and axial force
    required_area = moments / (0.87 * fy * (d - x))
    print("{sfasfsafsafsa",required_area)
    return required_area

doc = ezdxf.new(dxfversion='R2010') 
msp = doc.modelspace()
        
def beamdesign(moment,sigst,eff_depth ,dept_of_beam):
    result = ((round(moment, 3) * 10000000) / (sigst * (eff_depth - dept_of_beam / 10)))
    return result
def calculate_area(comb_data, sigst, eff_depth, depth_of_beam):
    area_data = {}
    for comb, levels in comb_data.items():
        area_data[comb] = {}
        for level, moment in levels.items():
            area = beamdesign(moment,sigst,eff_depth,depth_of_beam)
            area_data[comb][level] = round(area, 3)

    return area_data
def get_maximum_moments(data):
    maximum_moments = {}
    
    # Iterate through "COMB" combinations
    for comb, comb_data in data["col"].items():
        comb_maximums = {}
        
        # Iterate through levels in the "COMB" combination
        for level, level_data in comb_data.items():
            level_moments = []
            level_moments_min = []
            # Iterate through moments in the level
            for moment_data in level_data.values():
                level_moments.append(moment_data["Moment_max"])
                level_moments_min.append(moment_data["Moment_min"])
            # Find the maximum moment in the level
            maximum_moment = max(level_moments)
            minimum_moment =  min(level_moments_min)
            
            # Store the maximum moment for the level
            comb_maximums[level] = maximum_moment
        
        # Store the maximum moments for the "COMB" combination
        maximum_moments[comb] = comb_maximums
    
    return maximum_moments
def draw_rectangle(x, y, width, height,b,t1,t2):
    """
    Draws a rectangle using polylines in EZDFX.

    Args:
        x (float): The x-coordinate of the top-left corner of the rectangle.
        y (float): The y-coordinate of the top-left corner of the rectangle.
        width (float): The width of the rectangle.
        height (float): The height of the rectangle.
    """
    # Calculate the coordinates of the rectangle's corners
    x1 = x
    y1 = y
    x2 = x + width
    y2 = y
    x3 = x + width
    y3 = y + height
    x4 = x
    y4 = y + height

    # Draw the rectangle using polylines
    polyline = msp.add_lwpolyline([(x1, y1), (x4, y4), (x3, y3), (x2, y2), (x1, y1)])
    polyline.closed = True
    msp.add_aligned_dim(p1=(x1,y1), p2=(x1+b+2*t1, y1), distance=8000).render()
  
def draw_quad():
    x1 = 5000
    y1 = 5000
    a = 4000
    t1 = 1000 
    t2 = 300
    t4 = 500
    t3 = 200
    h = 3500
    l = 2500
    msp.add_lwpolyline([(x1,y1),(x1+a+2*t1+2*t2,y1),(x1+a+2*t1+2*t2,y1+t4),(x1+t1+2*t2+a,y1+t4),(x1+t1+t2+a+t3,y1+t4+h),(x1+t1+t2+a,y1+t4+h),(x1+t1+t2+a,y1+t4),(x1+t1+t2,y1+t4),(x1+t1+t2,y1+t4+h),(x1+t1+t2-t3,y1+t4+h),(x1+t1,y1+t4),(x1,y1+t4),(x1,y1)])
    
    msp.add_lwpolyline([(x1+t1+t2+a-t3,y1+t4+l),(x1+t1+t2+t3,y1+t4+l)])
app = Flask(__name__)
from ezdxf import new
@app.route('/check',methods=['GET','POST'])
def check():
    if request.method == 'GET':
        return "run"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
       

        
# Source rectangle coordinates: (0, 0) to (10, 5)
# Target rectangle coordinates: (2, 2) to (8, 7)
        # map_rectangle(msp, (0, 0), (10, 5), (2, 2), (8, 7))
        # x2 =  10000
        # y2 = 20000
        # b= 5000
        # a = 4000
        # t2 = 300
        # t1 = 1000
        # w= b + 2*t2 + 2*t1
        # h = a + 2*t1 + 2*t2
        # x3 = x2+t1
        # y3 = y2 + t1
        # w1 = b + 2*t2 
        # h1 = a + 2*t2

        # x1 = x2 + t1 + t2 
        # y1 =  y2 + t1+t2
        # w2 = b 
        # h2  = a
        # # msp.add_lwpolyline([(0,0), (10,5),(2,2),(8,7)])
        # draw_rectangle(x2,y2,w,h,t1,b,t2)
        # # draw_rectangle(x3,y3,w1,h1,t1,b,t2)
        # # draw_rectangle(x1,y1,w2,h2)


        # draw_quad()
        # doc.saveas('slab.dxf')
       
        
        # Load the workbook
        #######################################################################################################################
        ######################### excel stad ######################################################c
        # import xlwings as xw

        # # Load the workbook
        # workbook = xw.Book('oht.xlsm')

        # # Select the "std" sheet
        # std_sheet = workbook.sheets['std']

        # # Clear the range
        # std_sheet.range('A22:H395').clear()

        # # Get values from cells
        # noofcol = std_sheet.range('C2').value
        # stght = std_sheet.range('C3').value
        # noofbm = std_sheet.range('C4').value
        # fdndp = std_sheet.range('C5').value
        # colrd = std_sheet.range('C6').value
        # colsz = std_sheet.range('C7').value
        # tbwd = std_sheet.range('C8').value
        # tbdp = std_sheet.range('C9').value
        # bgwd = std_sheet.range('C10').value
        # bgdp = std_sheet.range('C11').value

        # noofjt = noofcol * (noofbm + 2) + 1
        # print("nofjt",noofjt)
        # var1 = 22 + 8 
        
        #  # Copy and paste values for part 1
        # std_sheet.range('J3:J11').copy()
        # std_sheet.range((22, 1)).paste()
        
        # # Part 2
        # for i in range(1, noofjt):
        #     std_sheet.range((var1 + i, 1)).value = i
        #     std_sheet.range((var1 + i, 2)).value = colrd
            
        #     temp1 = int(i / noofcol - 0.05) + 1
        #     if temp1 == 1:
        #         std_sheet.range((var1 + i, 3)).value = -fdndp
        #     else:
        #         std_sheet.range((var1 + i, 3)).value = (temp1 - 2) * stght / noofbm
        #     std_sheet.range((var1 + i, 4)).value = (i - 1) / noofcol * 360
        #     std_sheet.range((var1 + i, 5)).value = ";"
        
        # std_sheet.range((var1 + i, 1)).value = i
        # std_sheet.range((var1 + i, 2)).value = 0
        # std_sheet.range((var1 + i, 3)).value = stght + std_sheet.range('F2').value
        # std_sheet.range((var1 + i, 4)).value = 0
        # std_sheet.range((var1 + i, 5)).value = ";"
        
        # # Part 3
        # std_sheet.range('J12:J13').copy()
        # std_sheet.range((var1 + i + 1, 1)).paste()
        # i += 3
        # noofcolmemb = (noofbm + 1) * noofcol
        # noofbmmemb = noofcol * (noofbm + 1)
        
        # for j in range(1, noofcolmemb):
        #     std_sheet.range((var1 + i, 1)).value = j
        #     std_sheet.range((var1 + i, 2)).value = j
        #     std_sheet.range((var1 + i, 3)).value = j + noofcol
        #     std_sheet.range((var1 + i, 4)).value = ";"
        #     i += 1

        # # Save the workbook
        # workbook.save()
        # workbook.close()
        # import pandas as pd

        # # Read Excel file
        # df = pd.read_excel('oht.xlsm', sheet_name='std')

        # # Convert DataFrame to text
        # text_data = df.to_string(index=False)

        # # Write text data to a file
        # with open('output.txt', 'w') as file:
        #     file.write(text_data)

#         workbook = xw.Book('oht.xlsx')

# # Select the "std" sheet
#         sheet = workbook.sheets['std']
# # Select the "std" sheet
        
#         # Clear the range
#         sheet['A22:H395'].clear()

#         # Get values from cells
#         noofcol = sheet['C2'].value
#         stght = sheet['C3'].value
#         noofbm = sheet['C4'].value
#         fdndp = sheet['C5'].value
#         colrd = sheet['C6'].value
#         colsz = sheet['C7'].value
#         tbwd = sheet['C8'].value
#         tbdp = sheet['C9'].value
#         bgwd = sheet['C10'].value
#         bgdp = sheet['C11'].value
        
        
#         noofjt = noofcol * (noofbm + 2) + 1

#     # Open the text file for writing
#         with open('output.txt', 'w') as file:
#             file.write(f'noofcol: {noofcol}\n')
#             file.write(f'stght: {stght}\n')
#             file.write(f'noofbm: {noofbm}\n')
#             file.write(f'fdndp: {fdndp}\n')
#             file.write(f'colrd: {colrd}\n')
#             file.write(f'colsz: {colsz}\n')
#             file.write(f'tbwd: {tbwd}\n')
#             file.write(f'tbdp: {tbdp}\n')
#             file.write(f'bgwd: {bgwd}\n')
#             file.write(f'bgdp: {bgdp}\n')

#             # Write values from the sheet to the text file
#             file.write('\nFirst Part:\n')
#             for row in sheet.iter_rows(min_row=3, max_row=11, min_col=10, max_col=10):
#                 for cell in row:
#                     file.write(f'{cell.value}\n')

#             file.write('\nSecond Part:\n')
#             for i in range(1, noofjt):
#                 # Write the values for the second part to the text file
#                 file.write(f'{i}\t{colrd}\t')
#                 temp1 = int(i / noofcol - 0.05) + 1
#                 if temp1 == 1:
#                     file.write(f'{-fdndp}\t')
#                 else:
#                     file.write(f'{(temp1 - 2) * stght / noofbm}\t')
#                 file.write(f'{(i - 1) / noofcol * 360}\t;\n')

#             # Write values for the third part to the text file
#             file.write('\nThird Part:\n')
#             for row in sheet.iter_rows(min_row=12, max_row=13, min_col=10, max_col=10):
#                 for cell in row:
#                     file.write(f'{cell.value}\n')

#             i = 3
#             noofcolmemb = (noofbm + 1) * noofcol
#             noofbmmemb = noofcol * (noofbm + 1)

#             for j in range(1, noofcolmemb + 1):
#                 file.write(f'{j}\t{j}\t{j + noofcol}\t;\n')

    

#         model = FEModel3D()
#         radius = 500
#         num_col = 4
#         dx = 168.0
#         num_tie = 5
#         st = 15000
#         # Add nodes to the model
#         for i in range(num_col):
#             theta = 2 * i * 3.14159 / num_col
#             x = radius * (1 - dx / st) * pow(abs(math.cos(theta)), 0.8) * math.cos(theta)
#             y = radius * (1 - dx / st) * pow(abs(math.sin(theta)), 0.8) * math.sin(theta)
#             z = i * st / num_tie
#             model.add_node(f'N{i+1}', x, y, z)
###     Define a material
#         E = 29000       # Modulus of elasticity (ksi)
#         G = 11200       # Shear modulus of elasticity (ksi)
#         nu = 0.3        # Poisson's ratio
#         rho = 2.836e-4  # Density (kci)
#         model.add_material('Steel', E, G, nu, rho)
#         # Add columns to the model
#         for i in range(num_col):
#             if i == num_col - 1:
#                 j = 0
#             else:
#                 j = i + 1
#             model.add_member(f'M{i+1}', f'N{i+1}', f'N{j+1}')

#     # Add floor diaphragms to the model
#         for i in range(num_tie):
#             diaphragm_name = f'Diaphragm{i+1}'
#             for j in range(num_col):
#                 diaphragm_node = model.get_node(f'N{j+1}').translate(0, 0, i*st/num_tie)
#                 model.add_node(f'{diaphragm_name}_N{j+1}', diaphragm_node.X, diaphragm_node.Y, diaphragm_node.Z)
#             for j in range(num_col):
#                 if j == num_col - 1:
#                     k = 0
#                 else:
#                     k = j + 1
#                 model.add_member(f'{diaphragm_name}_M{j+1}', f'{diaphragm_name}_N{j+1}', f'{diaphragm_name}_N{k+1}')

#         # Print a summary of the model
#         model.summary()
        
    #     # Create a new finite element model
    #     beam = FEModel3D()

    #     # Add nodes (14 ft = 168 inches apart)
    #    #beam.add_node('N1', 00, 0, 0)
    #    # beam.add_node('N2', 168, 0, 0)
    #     radius = 500
    #     num_nodes = 4
    #     dx = 168.0
    #     num_tie = 5
    #     st = 15000
    #     num_cols =  4
    #     nodeCounter = 0 
    #     for i in range(num_cols):
    #         angle = i * (2 * math.pi / num_cols)
    #         x = radius * math.cos(angle)
    #         y = radius * math.sin(angle)
    #         beam.add_node(f'N{i+1}', x, y, 0)
    #         nodeCounter = i+1
    #     print("nodeCounter",nodeCounter)

    #     for j in range(num_cols):
    #         print("hereS")
    #         angle = j * (2 * math.pi / num_cols)
    #         x = radius * math.cos(angle)
    #         y = radius * math.sin(angle)
    #         beam.add_node(f'N{nodeCounter+1}', x, y, dx)
    #         nodeCounter = nodeCounter +1 
    #     for k in range(num_tie):
    #         for m in range(num_cols):
    #             angle = j* (2*math.pi/num_cols)
    #             x = radius * math.cos(angle)
    #             y = radius * math.sin(angle)
    #             beam.add_node(f'N{nodeCounter+1}', x, y, dx+ (k+1)*st/(num_tie+1))
    #             nodeCounter = nodeCounter +1 
                
    #     print("check me",nodeCounter)

    # #    for i in range(num_nodes):
    # #         #print('i in the loop',i)
            
    # #         x = radius * math.cos(angle)
    # #         y = radius * math.sin(angle)
    # #         node_name = 'N{}'.format(i+1)
    # #         print("i in the loop ",x,y)
    # #         beam.add_node(node_name, x, y, 0)
    # #     print("this is beam",beam,i)
    # #     temp = 4
    # #     for j in range(num_nodes):
    # #         angle = j* (2 * math.pi / num_nodes)
    # #         x = radius * math.cos(angle)
    # #         y = radius * math.sin(angle)
    # #         node_name1 = 'N{}'.format(temp+1)
    # #         temp = temp +1
    # #         print("j in the loop ",node_name1)
    # #         #print("i in the loop ",i+1)
    # #         beam.add_node(node_name1, x, y, dx)    


    #     # Define a material
    #     E = 29000       # Modulus of elasticity (ksi)
    #     G = 11200       # Shear modulus of elasticity (ksi)
    #     nu = 0.3        # Poisson's ratio
    #     rho = 2.836e-4  # Density (kci)
    #     beam.add_material('Steel', E, G, nu, rho)


    # #     # Add a beam with the following properties:
    # #     # Iy = 100 in^4, Iz = 150 in^4, J = 250 in^4, A = 20 in^2

    #     memberCounter  = 0
    #     print("numcounter here ",nodeCounter)
    #     beamCounter = 0
    #     extra = 1
    #     for i in range(num_tie+1):
    #         memberName = 'M{}'.format(i+1)
    #         mappedMember = 'M{}'.format(i+num_nodes +1)
    #         nodesName =  'N{}'.format(i+1)
    #         targetName = 'N{}'.format(i+num_nodes+1)
    #         print('member,nodeName,targetName',memberName,nodesName,targetName)
    #         memberCounter = memberCounter+1
    #         print("check i",i)
    #         #beam.add_member('M1', 'N1', 'N2', 'Steel', 100, 150, 250, 20)
    #         beam.add_member(memberName,nodesName,targetName,"Steel",100,150,250,20)
    #         for k in range(num_nodes):
    #             targetNode = 'N{}'.format(beamCounter+1)
    #             nextTarget = 'N{}'.format(extra+1)
    #             beamName = 'B{}'.format(beamCounter+1)
    #             beamCounter =  beamCounter+1
    #             extra =  extra +1
    #             beam.add_member( beamName,targetNode,nextTarget,"Steel",100,150,250,20)
    #     print("Member counter ", beamCounter,extra)

        
        
    #     # temp
    #     # temp2
    #     # for k in range(num_nodes):
    #     #     targetName = 'N{}'.format(k+1)
    #     #     newTarget = 'N{}'.format(num_nodes+k+1)
    #     #     newMember = 'B{}'.format(k+1)
    #     #     print("newMember",newMember,k)
    #     #     if newTarget == 'N{}'.format(2*num_nodes +1):
    #     #         newTarget = 'N{}'.format(num_nodes+1)
    #     #         print("in if else")
    #     #         beam.add_member(newMember,targetName,newTarget,"Steel",100,150,250,20)
    #     #         break 
    #     #     beam.add_member(newMember,targetName,newTarget,'Steel',100,150,250,20)
    #     #     temp = newtarget
    #     #     temp2 = newmember

        



    #    # beam.add_member('M1', 'N1', 'N5', 'Steel', 100, 150, 250, 20)
    #    # beam.add_member('M2', 'N2', 'N6', 'Steel', 100, 150, 250, 20)
    #    # beam.add_member('M3', 'N3', 'N7', 'Steel', 100, 150, 250, 20)
    #    # beam.add_member('M4', 'N4', 'N8', 'Steel', 100, 150, 250, 20)

    #     # Provide fixed supports

    #     for i in range(num_nodes):
    #         nodesName2 =  'N{}'.format(i+1)
    #         beam.def_support(nodesName2,True,True,True,True,True,True)

    #    # beam.def_support('N1', True, True, True, False, False, False)
    #    # beam.def_support('N2', True, True, True, True, False, False)
    #    # beam.def_support('N3', True, True, True, False, False, False)
    #    # beam.def_support('N4', True, True, True, True, False, False)



    #     # Add a uniform load of 200 lbs/ft to the beam (from 0 in to 168 in)
    #     beam.add_member_dist_load('M1', 'Fy', -200/1000/12, -200/1000/12, 0, 168)
    #     beam.add_member_dist_load('M2', 'Fy', -200/1000/12, -200/1000/12, 0, 168)
    #     beam.add_member_dist_load('M3', 'Fy', -200/1000/12, -200/1000/12, 0, 168)
    #     beam.add_member_dist_load('M4', 'Fy', -200/1000/12, -200/1000/12, 0, 168)

    #     # Alternatively the following line would do apply the load to the full
    #     # length of the member as well
    #     # beam.add_member_dist_load('M1', 'Fy', 200/1000/12, 200/1000/12)

    #     # Analyze the beam
        # beam.analyze()


    #     print("beammmmm",beam)

    #     # Print the shear, moment, and deflection diagrams
    #     beam.Members['M1'].plot_shear('Fy')
    #     beam.Members['M1'].plot_moment('Mz')
    #     beam.Members['M1'].plot_deflection('dy')

    #     beam.Members['M2'].plot_shear('Fy')
    #     beam.Members['M2'].plot_moment('Mz')
    #     beam.Members['M2'].plot_deflection('dy')

    #     beam.Members['M3'].plot_shear('Fy')
    #     beam.Members['M3'].plot_moment('Mz')
    #     beam.Members['M3'].plot_deflection('dy')

    #     beam.Members['M4'].plot_shear('Fy')
    #     beam.Members['M4'].plot_moment('Mz')
    #     beam.Members['M4'].plot_deflection('dy')

    #     # Print reactions at each end of the beam
    #     print('Node1:', beam.Nodes['N5'].RxnFY, 'kip')
    #     print('Node2', beam.Nodes['N6'].RxnFY, 'kip')
    #     print('Node3', beam.Nodes['N7'].RxnFY, 'kip')
    #     print('node4', beam.Nodes['N8'].RxnFY, 'kip')
    #     print('beamer Nodes', beam.Nodes)
        
    #     checkNode = beam.Nodes['N1']

    #     print('Node properties:')
    #     print('X:', checkNode.X)
    #     print('Y:', checkNode.Y)
    #     print('Z:', checkNode.Z)
    #     print('RxnFX:',checkNode.RxnFX)
    #     print('RxnFY:', checkNode.RxnFY)
    #     print('RxnFZ:', checkNode.RxnFZ)
    #     print('RxnMX:', checkNode.RxnMX)
    #     print('RxnMY:', checkNode.RxnMY)
    #     print('RxnMZ:', checkNode.RxnMZ)
    #   #  print('DX:', checkNode.DX)
    # #    print('DY:', checkNode.DY)
    #  #   print('DZ:', checkNode.DZ)
    #    # print('UX:', checkNode.UX)
    #   #  print('UY:', checkNode.UY)
    #     print('UZ:', checkNode.UZ)

    # Example of a simply supported beam with a uniform distributed load.
# Units used in this example are inches and kips
# This example does not use load combinations. The program will create a
# default load combindation called 'Combo 1'

# Import `FEModel3D` from `PyNite`
    

        # Create a new finite element model
        from PyNite import Plate3D
        beam = FEModel3D()
        radius = 236.22/2
        dx = 118.11
        num_tie = 4
        st = 629.921
        num_cols =  6
        nodeCounter = 0 
        for i in range(num_cols):
            angle = i * (2 * math.pi / num_cols)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            beam.add_node(f'N{i+1}', x, y, 0)
            nodeCounter = i+1
      

        for j in range(num_cols):
            print("hereS")
            angle = j * (2 * math.pi / num_cols)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            beam.add_node(f'N{nodeCounter+1}', x, y, dx)
            nodeCounter = nodeCounter +1 
        for k in range(num_tie):
            for m in range(num_cols):
                angle = m* (2*math.pi/num_cols)
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                beam.add_node(f'N{nodeCounter+1}', x, y, dx+ (k+1)*st/(num_tie+1))
                nodeCounter = nodeCounter +1 
        print("nodeCounter",nodeCounter)

      

        checkNode = beam.Nodes['N1']
        cant= 236/2 
        ver = 236/2
        ceiling_value  =  int((math.sqrt(cant**2+ver**2)/20))
        
        tankCounter = 1
        # for t in range(num_cols):
        #     angle =  t*(2*math.pi/num_cols)
        #     x1 = radius * math.cos(angle)
        #     y1 = radius * math.sin(angle)
        #     z1 = st+dx+(ver/ceiling_value+1)*t
        #     for p in range(ceiling_value):
        #         rad = (radius+(cant/ceiling_value+1)*p)
        #         x = rad * math.cos(p)
        #         y= rad*math.sin(p)
        # for k in range(ceiling_value):
        #     rad = radius + (cant/ceiling_value+1)*k
        #     x = rad * math.cos(k)
        #     y =  rad * math.sin(k)
        #     z=  st+dx+(ver/ceiling_value+1)*k
        #     beam.add_node('T{}'.format(tankCounter),x,y,z)
        #     tankCounter += 1
        #     for t in range(num_cols):
             
        #         beam.add_node('T{}'.format(tankCounter),x,y,z)
        #         print("tankCounterNode",tankCounter)
        #         tankCounter += 1
      
        level = 0  # Initialize the level counter
        levelCounter = 1 
        ceiling_value1 = (math.pi* 2*radius)/20
        PerLevelNodes =  int(ceiling_value1)
        if PerLevelNodes % 2 != 0:
            PerLevelNodes += PerLevelNodes +1
        print("odd boie bad boie",PerLevelNodes)
        wh =  180
        for k in range(int(ver/20)+1):
            # angle =  (2*math.pi/ceiling_value1)*k
            # rad = radius + (cant/ceiling_value+1)*k
            # x = rad * math.cos(angle)
            # y =  rad * math.sin(angle)
            diff =  ver/int(ver/20)
            print("In cone value ",k)
            print("celing value",ceiling_value)
            z = st + dx + diff * k  # Update z coordinate based on the current level
            
            # beam.add_node('L{}'.format(levelCounter), x, y, z)
            levelCounter += 1
            
            for t in range(int(ceiling_value1)):
                angle = t* (2*math.pi/ceiling_value1)
                rad = radius + ((diff*cant)/ver)*k
                # print("rad vale",rad)
                x = rad * math.cos(angle)
                y = rad * math.sin(angle)
                beam.add_node('T{}'.format(tankCounter), x, y, z)
                # print("tankCounterNode", tankCounter)
                tankCounter += 1
            
            # Check if the current level is at the ceiling value
        #     if (k + 1) % ceiling_value == 0:
        #         level += 1  # Increment the level counter
        # print("tank my counter",tankCounter)   
        
        # for node_key in beam.Nodes.keys():
        #     node = beam.Nodes[node_key]
        #     print(f"Node: {node_key}")
        #     print(f"X-coordinate: {node.X}")
        #     print(f"Y-coordinate: {node.Y}")
        #     print(f"Z-coordinate: {node.Z}")
        #     print()

        ################################################################################################
        ############################ tank wall ########################################################
        
        # for k in range(1,int(wh/20)):
                
        #     diff2 = wh/(int(wh/20))
        #     rad = radius + cant
        #     z = st+dx+ver+diff2*k
        #     for t in range(int(ceiling_value1)):
        #         angle = t* (2*math.pi/ceiling_value1)
               
        #         # print("rad vale",rad)
        #         x = rad * math.cos(angle)
        #         y = rad * math.sin(angle)
        #         beam.add_node('T{}'.format(tankCounter), x, y, z)
        #         # print("tankCounterNode", tankCounter)
        #         tankCounter += 1
        #############################################################################################
        ############################## tank bowl ######################################################
        harch1 = 120
        ht = dx + st + ver + wh + harch1
        # for k in range(int(harch1/20)):
        #     diff3 = harch1/int(harch1/20)
           
        #     z = dx +st+ver + wh + diff3*k
        #     rad =  math.sqrt((z-ht)/(-harch1/((radius+cant))**2))
        #     print("N TANK BOWL Loooop radd",rad)
        #     for t in range(int(ceiling_value1)):
        #         angle = t* (2*math.pi/ceiling_value1)
               
        #         # print("rad vale",rad)
        #         x = rad * math.cos(angle)
        #         y = rad * math.sin(angle)
        #         beam.add_node('T{}'.format(tankCounter), x, y, z)
        #         # print("tankCounterNode", tankCounter)
        #         tankCounter += 1
        # topNode = tankCounter - PerLevelNodes 
        # print("Top node ",topNode,tankCounter)
        # beam.add_node("S1",0,0,ht)   

        ###############################################################################
        ############################## tank lower Bowl #################################
        parc1 = 100
        tankBowl =0
        # print("tankBow1",tankBowl)
        # for k  in range(0,int(parc1/20)):
        #     diff4 = (parc1/int(parc1/20))
        #     httop = dx+st+parc1
        #     z = dx+st+diff4*k
        #     rad = math.sqrt(((z-httop)/(-parc1/(radius**2))))
        #     print("IN tankbowl lower")
        #     for t in range(int(ceiling_value1)):
        #         angle = t* (2*math.pi/ceiling_value1)
        #         print("In tankbowl lower 2")               
        #         # print("rad vale",rad)
        #         x = rad * math.cos(angle)
        #         y = rad * math.sin(angle)
        #         beam.add_node('TB{}'.format(tankBowl), x, y, z)
        #         tankBowl = tankBowl +1
                
                # print("tankCounterNode", tankCounter)
                
        print("Tank Bowl",tankBowl)
        
        diff4 = (parc1/int(parc1/20))
        height_of_special = dx+st + diff4*parc1/20
        
        # beam.add_node("NTB",0,0,height_of_special)
 
        # tankBowl =  tankBowl +1
        for z in range(nodeCounter):
            check = 'N{}'.format(z+1)
            temp =beam.Nodes[check]
            # print("coodinate of each nodeX:",check ,temp.X)
            # print("coodinate of each nodeY:",check, temp.Y)
            # print("coodinate of each nodeZ:",check,temp.Z)
        # Add nodes (14 ft = 168 inches apart)
       # beam.add_node('N1', 0, 0, 0)
       # beam.add_node('N2', 168, 0, 0)

       # Define a material
        E =  3150.002112909767 #29000       # Modulus of elasticity (ksi)
        G =   1346.1547119175743  #11200       # Shear modulus of elasticity (ksi)
        nu =  0.17 #0.3        # Poisson's ratio
        rho = 0.008679 # 2.836e-4  # Density (kci)
        beam.add_material('Steel', E, G, nu, rho)
        dbw2 = 300

        # Add a beam with the following properties:
        # Iy = 100 in^4, Iz = 150 in^4, J = 250 in^4, A = 20 in^2
        #beam.add_member('M1', 'N1', 'N2', 'Steel', 100, 150, 250, 20)
        #print(PyNite.__version__)
        offset_start = [0, 0, 10]  # [x, y, z] offset at the start of the member
        offset_end = [0, 0, -10] 

        # col prop
        iycol = 30568.33102
        izcol =15284.11746 
        Jcol =438.2525265 
        Acol =30580.51518

        iyb = 6768.7585
        izb =7507.842531 
        Jb =232.500465 
        Ab =6961.261985

        iyl = 66580.74882
        izl = 50678.05721
        Jl = 697.501395
        Al =69588.05659
        tankmembercounter = 1
        tanknode = tankCounter
        # beam.add_member('TM1','T1','T2','Steel',iycol,izcol,Jcol,Acol)
        # beam.add_member('TM2','T2','T3','Steel',iycol,izcol,Jcol,Acol)
        # beam.add_member('TM3','T3','T4','Steel',iycol,izcol,Jcol,Acol)
        # beam.add_member('TM4','T4','T5','Steel',iycol,izcol,Jcol,Acol)
        # beam.add_member('TM5','T5','T6','Steel',iycol,izcol,Jcol,Acol)
        # for i  in range(topNode,tankCounter):
        #     beam.add_member("STN{}".format(i),"S1", "T{}".format(i),'Steel',iycol,izcol,Jcol,Acol) 
        t =10
        material ="Steel"
        # for k in range(1,tankCounter-1):
        #     beam.add_member("MT{}".format(k),"T{}".format(k),"T{}".format(k+1),'Steel',iycol,izcol,Jcol,Acol)
        #     # beam.add_quad("P{}".format(k),"T{}".format(k),"T{}".format(k+1),"T{}".format(k+1),"T{}".format(i+PerLevelNodes+1),t,material,1.0,1.0)
        print("}}}}}",tanknode)
        # for f in range(1,levelCounter-1):
        #     beam.add_member("LT{}".format(f+1),"L{}".format(f),"L{}".format(f+1),'Steel',iycol,izcol,Jcol,Acol)
        # print("tank counter node",tankCounter)
        tankCounter = tankCounter -1
        print("perlevelNode",PerLevelNodes)
        for z in range(1,int(tankCounter-PerLevelNodes)+1):
            # print("IN MY Plate Loopp",z,z+1,z+PerLevelNodes+1,z+PerLevelNodes)
            if(z % PerLevelNodes == 0):
                beam.add_quad("PL{}".format(z),"T{}".format(z),"T{}".format(z-PerLevelNodes+1),"T{}".format(z+1),"T{}".format(z+PerLevelNodes),t,material,1.0,1.0)
            else:
                beam.add_quad("PL{}".format(z),"T{}".format(z),"T{}".format(z+1),"T{}".format(z+PerLevelNodes+1),"T{}".format(z+PerLevelNodes),t,material,1.0,1.0)
        
        # for x in range(1,int(tankBowl-PerLevelNodes)):
        #     if x in range(1,PerLevelNodes):
        #         if x == PerLevelNodes:
        #             beam.add_quad("PBL{}".format(x),"T{}".format(x),"T1","TB{}".format(z),"TB1",t,material,1.0,1.0)
        #         else:
        #             beam.add_quad("PBL{}".format(x),"T{}".format(x),"T{}".format(x+1),"TB{}".format(x+1),"TB{}".format(x),t,material,1.0,1.0) 
        #     else:
        #         if(x % PerLevelNodes == 0):
        #             beam.add_quad("PBL{}".format(x),"TB{}".format(x),"TB{}".format(x-PerLevelNodes+1),"TB{}".format(x+1),"TB{}".format(x+PerLevelNodes),t,material,1.0,1.0)
        #         else:
        #             beam.add_quad("PBL{}".format(x),"TB{}".format(x),"TB{}".format(x+1),"TB{}".format(x+PerLevelNodes+1),"TB{}".format(x+PerLevelNodes),t,material,1.0,1.0)

        PlatCounter = 1
        for k in range(0,tankBowl-1):
            beam.add_member("SPP{}".format(k),"TB{}".format(k),"TB{}".format(k+1),"Steel",iyb, izb, Jb, Ab)
        
        print("TBBBBB186",beam.Nodes.keys())
        PerLevelNodes = 37
        per_level_node = 36
        nameCounter = 1
        temp = 1
        # for level in range(int(parc1/20)-1):
        #     start_node = level * PerLevelNodes
        #     for i in range(start_node, start_node + PerLevelNodes+2):
    
        #         # Get the four corner nodes to create the quad plate
        #         if(i == 0):
        #             node1 = 'TB{}'.format(i)
        #             node2 = 'TB{}'.format(i + 1)
        #             node3 = 'TB{}'.format(i + 1+ PerLevelNodes)
        #             node4 ='TB{}'.format(i +PerLevelNodes)
        #             print("if value of each nodes 0",node1,node2,node3,node4)
        #         elif((i+1) % PerLevelNodes == 0): 
        #             if(i==148):
        #                 break
        #             print("IN multiple of valu",i,PerLevelNodes)             
        #             node1 = 'TB{}'.format(i)
        #             node2 = 'TB{}'.format(i-per_level_node)
        #             node3 = 'TB{}'.format(i +1)
        #             node4 = 'TB{}'.format(i + PerLevelNodes)
        #             print("else if value of each nodes1111111" ,i,node1,node2,node3,node4)
        #         else:
        #             if(i==148):
        #                 break
        #             node1 = 'TB{}'.format(i)
        #             node2 = 'TB{}'.format(i + 1)
        #             node3 = 'TB{}'.format(i + 1 + PerLevelNodes)         
        #             node4 ='TB{}'.format(i +PerLevelNodes)
        #             print("did that condioton become false",level,i)
        #             print("else value of each nodes",node1,node2,node3,node4)
                   
        #             # Create a new quad plate between the nodes
        #         beam.add_quad('Plate{}'.format(nameCounter), node1, node2, node3, node4, t=1.0, material='Steel')  # Adjust t and material as needed
        #         nameCounter += 1
            


        # for u in range(nameCounter,int((parc1/20))*PerLevelNodes-1):
        #     beam.add_member("MTB{}".format(u),"TB{}".format(u),"TB{}".format(u+1),'Steel',iycol,izcol,Jcol,Acol)
        
                 
        # for k in range(int(parc1/20)-1):
        #     print("Cancer",k)
        #     for z in range(k,PerLevelNodes):
                
        #         print( 'bhosikda ',z)
        #         if k == 0:
        #             if(z  == PerLevelNodes):
        #                 print('+++++>t 2 value at if and 2 tb',z,1,z,1)
        #                 print("IN MY Plate Loopp",z,z-PerLevelNodes+1,z+PerLevelNodes)
        #                 beam.add_quad("PLB{}".format(k),"T{}".format(z+1),"T{}".format(1),"TB{}".format(1),"TB{}".format(z+1),t,material,1.0,1.0)
                        
        #             else:
        #                 beam.add_quad("PLB{}".format(k),"T{}".format(z+1),"T{}".format(z+2),"TB{}".format(z+2),"TB{}".format(z+1),t,material,1.0,1.0)
        #         else:    
        #             if(z == PerLevelNodes):
                        
        #                 beam.add_quad("PLB{}".format(k),"TB{}".format(z+1+PerLevelNodes*(k-1)),"TB{}".format(PerLevelNodes*(k-1)),"TB{}".format(((k-1)+1)*PerLevelNodes+1),"TB{}".format(((k-1)+1)*PerLevelNodes),t,material,1.0,1.0)
                        
        #             else:
        #                 beam.add_quad("PLB{}".format(k),"TB{}".format(z+1+PerLevelNodes*(k-1)),"TB{}".format(z+2+PerLevelNodes*(k-1)),"TB{}".format(((k-1)+1)*PerLevelNodes+z+2),"TB{}".format(((k-1)+1)*PerLevelNodes),t,material,1.0,1.0)
                       
        ##################################################################################################################
        #################### add quad for tank wall ###################################################################

        thick = 20


        # for z in range(1,int(tankWall-PerLevelNodes)):
        #     # print("IN MY Plate Loopp",z,z+1,z+PerLevelNodes+1,z+PerLevelNodes)
        #     if(z % PerLevelNodes == 0):
                
        #         beam.add_quad("PW{}".format(z),"T{}".format(z),"T{}".format(z-PerLevelNodes+1),"T{}".format(z+1),"T{}".format(z+PerLevelNodes),thick,material,1.0,1.0)
        #     else:
        #         beam.add_quad("PW{}".format(z),"T{}".format(z),"T{}".format(z+1),"T{}".format(z+PerLevelNodes+1),"T{}".format(z+PerLevelNodes),thick,material,1.0,1.0)
        
        # for z in range(1,tanknode-1):
        #     print("}}}}}",z)
            
        #     beam.add_member('TM{}'.format(tankmembercounter),'T{}'.format(z),"T{}".format(z+1),'Steel',iycol,izcol,Jcol,Acol)
        #     print("tank member counter",tankmembercounter,z,z+1)
        #     tankmembercounter =  tankmembercounter +1
        #     tanknode =  tanknode +1 
        print("IN the looooooooooooooooooooooop")




        # beam.add_quad("TEMPPLATE","T2","T3","T","T39",t,material)

        # beam.add_quad_surface_pressure("Plate1",pressure=10,case='SC')

        # beam.add_load_combo("SC1",factors={"SC":1})

        print("all cases of pressure==========================================================>", beam.LoadCases)
        # for node_key in beam.Nodes.keys():
        #     node = beam.Nodes[node_key]
        #     print(f"Node: {node_key}")
        #     print(f"X-coordinate: {node.X}")
        #     print(f"Y-coordinate: {node.Y}")
        #     print(f"Z-coordinate: {node.Z}")
        #     print()
            
        

    #     for element in beam.Plates.values():
    # # Check if the element is a quad element
            
    #         print("Quad Name:", element.Name)
    #         print("Node 1:", element.iNode)
    #         print("Node 2:", element.jNode)
    #         print("Node 3:", element.mNode)
    #         print("Node 4:", element.nNode)
    #         print("Thickness:", element.t)
    #         print("Material:", element.material)
    #    
    #      print()
        nearNumber =  nearest_multiple(int((2*math.pi*radius)/20),num_cols)
        print("Near Number",nearNumber)
        for i in range(0,nearNumber):
            angle =  (2*math.pi/nearNumber)*i
            x=radius*math.cos(angle)
            y= radius*math.sin(angle)
            z= dx+st
            beam.add_node("LS{}".format(i),x,y,z)


        number_of_col = (num_tie+1)*num_cols 
        
        print("num_col",number_of_col)
        counterNumberofCol = 0
        lscounter = 0
        for l in range(number_of_col+num_cols):
            # print("printl ",l)
            # print("meamber Name",l+1)
            # print("first target",l+1)
            # print("second target node",l+num_cols+1)
            print("value ",l)
            if l >=  number_of_col:
                if lscounter*int((nearNumber/num_cols)) ==  nearNumber:
                    beam.add_member('MLS{}'.format(l+1),'N{}'.format(l+1),'LS{}'.format(0),'Steel',iycol,izcol,Jcol,Acol)
                    lscounter += 1
                else:
                    beam.add_member('MLS{}'.format(l+1),'N{}'.format(l+1),'LS{}'.format(lscounter*int((nearNumber/num_cols))),'Steel',iycol,izcol,Jcol,Acol)
                    lscounter += 1
            else:
                beam.add_member('MLS{}'.format(l+1),'N{}'.format(l+1),'N{}'.format(l+num_cols+1),'Steel',iycol,izcol,Jcol,Acol)
                counterNumberofCol = counterNumberofCol+1
                print("mapping col")        

        # print("number vertical col ", counterNumberofCol)

        golbalCounter = counterNumberofCol


        counterNumberofCol = counterNumberofCol+1

        # add horizontal memebers 
        virticalCounter = counterNumberofCol
        for m  in range(1,num_tie+2):

            if m == num_tie+3:
            
                for p in range(1,num_cols+1):
                    if p == num_cols:
                        beam.add_member('M{}'.format(counterNumberofCol),'N{}'.format(num_cols+p+(m-1)*num_cols),'N{}'.format(num_cols+1+p+(m-2)*num_cols),"Steel",iyb, izb, Jb, Ab)
                        virticalCounter = virticalCounter+1
                        counterNumberofCol = counterNumberofCol +1
                    else:
                        extra1 = num_cols+p+(m-1)*num_cols
                        extra2 = num_cols+1+p+(m-1)*num_cols
                        # print('nodes 1',extra1)
                        # print('nodes 2 ',extra2)
                        beam.add_member('M{}'.format(counterNumberofCol),'N{}'.format(num_cols+p+(m-1)*num_cols),'N{}'.format(num_cols+1+p+(m-1)*num_cols),"Steel",iyb, izb, Jb, Ab)
                        virticalCounter = virticalCounter+1
                        counterNumberofCol = counterNumberofCol +1 
            for p in range(1,num_cols+1):
                    if p == num_cols:
                        beam.add_member('M{}'.format(counterNumberofCol),'N{}'.format(num_cols+p+(m-1)*num_cols),'N{}'.format(num_cols+1+p+(m-2)*num_cols),"Steel",iyb, izb, Jb, Ab)
                        virticalCounter = virticalCounter+1
                        counterNumberofCol = counterNumberofCol +1
                    else:
                        extra1 = num_cols+p+(m-1)*num_cols
                        extra2 = num_cols+1+p+(m-1)*num_cols
                        # print('nodes 1',extra1)
                        # print('nodes 2 ',extra2)
                        beam.add_member('M{}'.format(counterNumberofCol),'N{}'.format(num_cols+p+(m-1)*num_cols),'N{}'.format(num_cols+1+p+(m-1)*num_cols),"Steel",iyb, izb, Jb, Ab)
                        virticalCounter = virticalCounter+1
                        counterNumberofCol = counterNumberofCol +1 


        lastCircleCounter =  nodeCounter - num_cols 
        
        
        print("horizontal++++++++++++++++++++++++++++++++++++++++++>",virticalCounter,lastCircleCounter,type(nearNumber))    

      

        for j in range(0,nearNumber):
            print("JJJ++++++++>",j)
            if j == nearNumber -1:
                beam.add_member("MS{}".format(j),"LS{}".format(j),"LS{}".format(0),"Steel",iyb,izb,Jb,Ab)
            else:
                beam.add_member("MS{}".format(j),"LS{}".format(j),"LS{}".format(j+1),"Steel",iyb, izb, Jb, Ab)    
        
        # Provide simple supports
        # beam.def_support('N1', True, True, True, False, False, False)
        # beam.def_support('N2', True, True, True, True, False, False)
        
        for i in range(num_cols):
            nodesName2 =  'N{}'.format(i+1)
            beam.def_support(nodesName2,True,True,True,True,True,True)

        # Add a uniform load of 200 lbs/ft to the beam (from 0 in to 168 in)
        #beam.add_member_dist_load('M1', 'Fy', -200/1000/12, -200/1000/12, 0, 168)

        # totalNumberOfNode =  (num_cols*(num_tie+2))
        # print("Number of the node",totalNumberOfNode)
        # for v in range(totalNumberOfNode-num_cols,totalNumberOfNode):
        #     beam.add_node_load('N{}'.format(v),"FX",100,"CASE 1")

        #beam.add_node('S1', 0, 0, st+dx)
        #beam.add_node_load("N54","FX",-100.0)
        # Alternatively the following line would do apply the load to the full
        # length of the member as well
        # # beam.add_member_dist_load('M1', 'Fy', 200/1000/12, 200/1000/12)
        # temp = nodeCounter
        # remberNode =  temp
        # beam.add_node("S1",0,0,st+dx)
        # for i in range(num_cols):
        #     beam.add_member("H{}".format(i+10),"S1",'N{}'.format(nodeCounter),"Steel",iyl, izl, Jl, Al)
        #     nodeCounter = nodeCounter-1
        # beam.add_node_load("S1","FY",22.046226218)       # Analyze the beam
         # Density of the material in lb/ft^3

            #weight = element.get_volume() * density * 9.8  # Calculate the weight based on the element's volume
            #beam.add_member_dist_load(element.Name, 'Fz', -weight) 


        #############################################################################################
        ########## ADDING self wieght in sturcture ###########################
        # colnodecounter = 0 
        # for l in range(number_of_col):
        #     weight = Acol * rho
        #     beam.add_member_dist_load('M{}'.format(l+1), 'FZ', -weight,-weight,case='DeadLoad') 

        #     colnodecounter = colnodecounter+1

        # colnodecounter = colnodecounter +1    
        # for m  in range(1,num_tie+3):

        #     if m == num_tie+3:
            
        #         for p in range(1,num_cols+1):
        #             if p == num_cols:
        #                 weight1 = Ab * rho
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter), 'FZ', -weight1,-weight1,case='DeadLoad') 
        #             #  virticalCounter = verticalCounter+1
        #                 colnodecounter = colnodecounter +1
        #             else:
        #                 weight1 = Ab * rho
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter), 'FZ', -weight1,-weight1,case='DeadLoad') 
        #             # virticalCounter = virticalCounter+1
        #                 colnodecounter = colnodecounter +1 
        #     for p in range(1,num_cols+1):
        #             if p == num_cols:
        #                 weight1 = Ab * rho
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter), 'FZ', -weight1,-weight1,case='DeadLoad') 
                   
        #                 colnodecounter = colnodecounter +1
        #             else:
        #                 weight1 = Ab * rho
                       
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter), 'FZ', -weight1,-weight1,case='DeadLoad') 
        #             # virticalCounter = virticalCounter+1
        #                 colnodecounter = colnodecounter +1 
        #######################################################
        ############## uniform load on member ##############
        # print("for uniform load",counterNumberofCol)
        # temp2 = counterNumberofCol 
        # # print("temp21",temp2)
        # temp2 =  temp2 - num_cols
        # # print("temp2 ",temp2)
        # for i in range(num_cols):
        #     weight3 = 100
        #     # print("UIL FZ ",temp2)
        #     beam.add_member_dist_load('M{}'.format(temp2), 'FZ', -weight3,-weight3,case='DeadLoad')
        #     temp2 = temp2+1

        # print("my load ", beam.LoadCases)
      #  beam.add_load_combo("Dead",factors={'U':1,'W':1},combo_type="strength")
        
        ##################################################################################################
        #################################### DeadLoad2 ##################################################
        # colnodecounter1 = 0 
        # for l in range(number_of_col):
        #     weight = Acol * rho
        #     beam.add_member_dist_load('M{}'.format(l+1), 'FZ', -weight,-weight,case='DeadLoad2') 

        #     colnodecounter1 = colnodecounter1+1

        # colnodecounter1 = colnodecounter1 +1    
        # for m  in range(1,num_tie+3):

        #     if m == num_tie+3:
            
        #         for p in range(1,num_cols+1):
        #             if p == num_cols:
        #                 weight1 = Ab * rho
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter1), 'FZ', -weight1,-weight1,case='DeadLoad2') 
        #             #  virticalCounter = verticalCounter+1
        #                 colnodecounter1 = colnodecounter1 +1
        #             else:
        #                 weight1 = Ab * rho
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter1), 'FZ', -weight1,-weight1,case='DeadLoad2') 
        #             # virticalCounter = virticalCounter+1
        #                 colnodecounter1 = colnodecounter1 +1 
        #     for p in range(1,num_cols+1):
        #             if p == num_cols:
        #                 weight1 = Ab * rho
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter1), 'FZ', -weight1,-weight1,case='DeadLoad2') 
                   
        #                 colnodecounter1 = colnodecounter1 +1
        #             else:
        #                 weight1 = Ab * rho
                       
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter1), 'FZ', -weight1,-weight1,case='DeadLoad2') 
        #             # virticalCounter = virticalCounter+1
        #                 colnodecounter1 = colnodecounter1 +1 
        #######################################################
        ############## uniform load on member ##############
        # print("for uniform load",counterNumberofCol)
        # temp2 = counterNumberofCol
        # # print("temp21",temp2)
        # temp2 =  temp2 - num_cols
        # print("temp2 ",temp2)
        # for i in range(num_cols):
        #     weight3 = 100
        #     # print("UIL FZ ",temp2)
        #     beam.add_member_dist_load('M{}'.format(temp2), 'FZ', -weight3,-weight3,case='DeadLoad2')
        #     temp2 = temp2+1

        # print("my load ", beam.LoadCases)


        ###############################################################
        #### wind load case ############ on both beams and col ############

        # WindloadCounter= num_cols
        # for l in range(num_cols,number_of_col):
        #     weight = 10
        #     beam.add_member_dist_load('M{}'.format(l+1), 'FY', weight,weight,case="WL") 

        #     WindloadCounter = WindloadCounter+1


        # colnodecounter = 0 
        # for l in range(num_cols, number_of_col):
        #     weight = 10
        #     beam.add_member_dist_load('M{}'.format(l+1), 'FY', weight,weight,case="WL") 

        #     colnodecounter = colnodecounter+1

        # colnodecounter = colnodecounter +1    
        # for m  in range(1,num_tie+3):

        #     if m == num_tie+3:
            
        #         for p in range(1,num_cols+1):
        #             if p == num_cols:
        #                 weight1 = 10
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter), 'FY', weight1,weight1,case="WL") 
        #             #  virticalCounter = verticalCounter+1
        #                 colnodecounter = colnodecounter +1
        #             else:
        #                 weight1 = 10
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter), 'FY', weight1,weight1,case="WL") 
        #             # virticalCounter = virticalCounter+1
        #                 colnodecounter = colnodecounter +1 
        #     for p in range(1,num_cols+1):
        #             if p == num_cols:
        #                 weight1 = 10
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter), 'FY', weight1,weight1,case="WL") 
                   
        #                 colnodecounter = colnodecounter +1
        #             else:
        #                 weight1 = 10
                       
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter), 'FY', weight1,weight1,case="WL") 
        #             # virticalCounter = virticalCounter+1
        #                 colnodecounter = colnodecounter +1


        ############################################
        ## Add Wind load to last nodes ######################
        # print("node counte late",nodeCounter)

        # windNodeCounter =  remberNode 
        # windNodeCounter =  windNodeCounter -  num_cols +1
        # # print("wind counter",windNodeCounter)
        # for g in  range(num_cols):
        #     # print("Node in wind",g)
        #     # print("N{}".format(windNodeCounter))
        #     beam.add_node_load('N{}'.format(windNodeCounter),'MY',1000,case="WLN")
        #     windNodeCounter =  windNodeCounter +1
        # Apply loads for Combo 1
 

        #beam.add_load_combo("Wind",{'WL':1,'WLN':1})
        #beam.add_load_combo('1.4F', {'U': 1.4})
        #be am.add_load_combo("DeadWeight",factors={'SelfWeight':1,'UniFZ':1},combo_type='strength' )
        #beam.add_load_combo('1.2D+1.0SelfWeight', factors={'D':1.2, 'W':1.0})
        ###############################################################################
        ############################## WINDLOAD (x)###################################
        ################### load on last node where it FX #########################
        # windNodeCounter1 =  remberNode 
        # windNodeCounter1 =  windNodeCounter1 -  num_cols +1
        # # print("wind counter",windNodeCounter1)
        # for g in  range(num_cols):
        #     # print("Node in wind",g)
        #     # print("N{}".format(windNodeCounter1))
        #     beam.add_node_load('N{}'.format(windNodeCounter1),'FX',1000,case="WLX")
        #     windNodeCounter1 =  windNodeCounter1 +1
        ######################## load on last node it MY #################
        # windNodeCounter2 =  remberNode 
        # windNodeCounter2 =  windNodeCounter2 -  num_cols +1
        # print("wind counter",windNodeCounter2)
        # for g in  range(num_cols):
        #     # print("Node in wind",g)
        #     # print("N{}".format(windNodeCounter2))
        #     beam.add_node_load('N{}'.format(windNodeCounter2),'MY',1000,case="WLX")
        #     windNodeCounter2 =  windNodeCounter2 +1    
        ################################ Unifrom load on beam and col ###########

        # colnodecounter1 = 0 
        # for l in range(num_cols, number_of_col):
        #     weight = 10
        #     beam.add_member_dist_load('M{}'.format(l+1), 'FY', weight,weight,case="WLX") 
        #     # print("=====>>> ","M{}".format(l+1))
        #     colnodecounter1 = colnodecounter1+1

        # colnodecounter1 = colnodecounter1 +1    
        # for m  in range(1,num_tie+3):
        #     # print("In my loop1")
        #     if m == num_tie+3:
        #         # print("In my loop2")
        #         for p in range(1,num_cols+1):
        #             # print("In my loop3")
        #             if p == num_cols:
        #                 weight1 = 10
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter1), 'FY', weight1,weight1,case="WLX") 
        #             #  virticalCounter = verticalCounter+1
        #                 colnodecounter1 = colnodecounter1 +1
        #             else:
        #                 # print("In my loop4")
        #                 weight1 = 10
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter1), 'FY', weight1,weight1,case="WLX") 
        #             # virticalCounter = virticalCounter+1
        #                 colnodecounter1 = colnodecounter1 +1 
        #     for p in range(1,num_cols+1):
        #             # print("In my loop5")
        #             if p == num_cols:
        #                 weight1 = 10
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter1), 'FY', weight1,weight1,case="WLX") 
                   
        #                 colnodecounter1 = colnodecounter1 +1
        #             else:
        #                 weight1 = 10
                       
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter1), 'FY', weight1,weight1,case="WLX") 
        #             # virticalCounter = virticalCounter+1
        #                 colnodecounter1 = colnodecounter1 +1
        #beam.add_load_combo("WindX",{"WLX":1}) 
        ###############################################################################
        # ####################### Wind Load FUll tank ################################
         ################### load on last node where it FZ #########################
        # windNodeCounter4 =  remberNode 
        # windNodeCounter4 =  windNodeCounter4 -  num_cols +1
        # # print("wind counter",windNodeCounter4)
        # for g in  range(num_cols):
        #     # print("Node in wind",g)
        #     # print("N{}".format(windNodeCounter1))
        #     beam.add_node_load('N{}'.format(windNodeCounter4),'FY',1000,case="WLFT")
        #     windNodeCounter4 =  windNodeCounter4 +1
        ######################## load on last node it MX #################
        # windNodeCounter5 =  remberNode 
        # windNodeCounter5 =  windNodeCounter5 -  num_cols +1
        # # print("wind counter",windNodeCounter5)
        # for g in  range(num_cols):
        #     # print("Node in wind",g)
        #     # print("N{}".format(windNodeCounter5))
        #     beam.add_node_load('N{}'.format(windNodeCounter5),'MY',1000,case="WLFT")
            
        #     windNodeCounter5 =  windNodeCounter5 +1    
        ############################## uniform load on beam and col #################
        # colnodecounter2 = num_cols
        # for l in range(num_cols, number_of_col):
        #     weight = 10
        #     beam.add_member_dist_load('M{}'.format(l+1), 'FY', weight,weight,case="WLFT") 
        #     # print("===>","M{}".format(l+1))
        #     colnodecounter2 = colnodecounter2+1

        # colnodecounter2 = colnodecounter2 +1   
        # # print("Col counter chekc",colnodecounter2) 
        # for m  in range(1,num_tie+3):

        #     if m == num_tie+3:
            
        #         for p in range(1,num_cols+1):
        #             if p == num_cols:
        #                 weight1 = 10
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter2), 'FY', weight1,weight1,case="WLFT") 
        #                 print("=>>>>","M.{}".format(colnodecounter2))
        #             #  virticalCounter = verticalCounter+1
        #                 colnodecounter2 = colnodecounter2 +1
        #             else:
        #                 weight1 = 10
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter2), 'FY', weight1,weight1,case="WLFT")
        #                 print("=>>>>","M.{}".format(colnodecounter2)) 
        #             # virticalCounter = virticalCounter+1
        #                 colnodecounter2 = colnodecounter2 +1 
        #     for p in range(1,num_cols+1):
        #             if p == num_cols:
        #                 weight1 = 10
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter2), 'FY', weight1,weight1,case="WLFT") 
        #                 print("=>>>>","M.{}".format(colnodecounter2))
        #                 colnodecounter2 = colnodecounter2 +1
        #             else:
        #                 weight1 = 10
                       
        #                 beam.add_member_dist_load('M{}'.format(colnodecounter2), 'FY', weight1,weight1,case="WLFT")
        #                 print("=>>>>","M.{}".format(colnodecounter2)) 
        #             # virticalCounter = virticalCounter+1
        #                 colnodecounter1 = colnodecounter +1 
        # beam.add_load_combo("WLFULL",{"WLFT":1})                        
        ##############################################################################
        ################################# EQ load ####################################
        # earthCouter =  remberNode 
        # earthCouter =  earthCouter -  num_cols +1
        # print("wind counter",windNodeCounter)
        # for g in  range(num_cols):
        #     print("Node in wind",g)
        #     print("N{}".format(earthCouter))
        #     beam.add_node_load('N{}'.format(earthCouter),'FX',1000,case="EQFT")
        #     earthCouter =  earthCouter +1

        # earthFullCouter =  remberNode 
        # earthFullCouter =  earthFullCouter -  num_cols +1
        # print("wind counter",windNodeCounter)
        # for g in  range(num_cols):
        #     print("Node in wind",g)
        #     print("N{}".format(earthFullCouter))
        #     beam.add_node_load('N{}'.format(earthFullCouter),'MZ',-1000,case="EQFT")
        #     earthFullCouter =  earthFullCouter +1
        ##################################################################################
        ################################## EQ LOAD #####################################
        # earthCouter1 =  remberNode 
        # earthCouter1 =  earthCouter1 -  num_cols +1
        # print("wind counter",windNodeCounter)
        # for g in  range(num_cols):
        #     print("Node in wind",g)
        #     print("N{}".format(earthCouter1))
        #     beam.add_node_load('N{}'.format(earthCouter1),'FZ',1000,case="EQ")
        #     earthCouter1 =  earthCouter1 +1

        # earthFullCouter1 =  remberNode 
        # earthFullCouter1 =  earthFullCouter1 -  num_cols +1
        # print("wind counter",windNodeCounter)
        # for g in  range(num_cols):
        #     print("Node in wind",g)
        #     print("N{}".format(earthFullCouter1))
        #     beam.add_node_load('N{}'.format(earthFullCouter1),'MX',-1000,case="EQ")
        #     earthFullCouter1 =  earthFullCouter1 +1
       # beam.add_load_combo("EarthQFullTank",{'EQFT':1,'DeadLoad':1})

        # beam.add_load_combo("COMB1",{"DeadLoad":1.5})
        # beam.add_load_combo("COMB2",{"DeadLoad2":1})
        # beam.add_load_combo("COMB3",{"DeadLoad":1.5,"WLX":1.5})
        # beam.add_load_combo("COMB4",{"DeadLoad":1.5,"WLFT":1.5})
        # beam.add_load_combo("COMB5",{"DeadLoad":1.5,"WLX":-1.5})
        # beam.add_load_combo("COMB6",{"DeadLoad":1.5,"WLFT":-1.5})
        # beam.add_load_combo("COMB7",{"DeadLoad2":1.5,"WLX":1.5})
        # beam.add_load_combo("COMB8",{"DeadLoad2":1.5,"WLFT":1.5})
        # beam.add_load_combo("COMB9",{"DeadLoad2":1.5,"WLX":-1.5})
        # beam.add_load_combo("COMB10",{"DeadLoad2":1.5,"WLFT":-1.5})

        # beam.add_load_combo("COMB11",{"DeadLoad":0.9,"WLX":1.5})
        # beam.add_load_combo("COMB12",{"DeadLoad":0.9,"WLFT":1.5})
        # beam.add_load_combo("COMB13",{"DeadLoad":0.9,"WLX":-1.5})
        # beam.add_load_combo("COMB14",{"DeadLoad":0.9,"WLFT":1.5})
        # beam.add_load_combo("COMB15",{"DeadLoad2":0.9,"WLX":1.5})
        # beam.add_load_combo("COMB16",{"DeadLoad2":0.9,"WLFT":1.5})
        # beam.add_load_combo("COMB17",{"DeadLoad2":0.9,"WLX":-1.5})
        # beam.add_load_combo("COMB18",{"DeadLoad2":0.9,"WLFT":-1.5})
        # beam.add_load_combo("COMB19",{"DeadLoad":1.5,"EQFT":1.5})
        # beam.add_load_combo("COMB20",{"DeadLoad":1.5,"EQ":1.5})
        # beam.add_load_combo("COMB21",{"DeadLoad":1.5,"EQFT":-1.5})
        # beam.add_load_combo("COMB22",{"DeadLoad":1.5,"EQ":-1.5})
        # beam.add_load_combo("COMB23",{"DeadLoad":0.9,"EQFT":1.5})
        # beam.add_load_combo("COMB24",{"DeadLoad":0.9,"EQ":1.5})
        # beam.add_load_combo("COMB25",{"DeadLoad":0.9,"EQ":-1.5})
        # beam.add_load_combo("COMB26",{"DeadLoad":0.9,"EQFT":-1.5})
        # beam.add_load_combo("COMB27",{"DeadLoad":1.2,"WLX":1.2})
        # beam.add_load_combo("COMB28",{"DeadLoad":1.2,"WLFT":1.2})
        # beam.add_load_combo("COMB29",{"DeadLoad":1.2,"WLX":-1.2})
        # beam.add_load_combo("COMB30",{"DeadLoad":1.2,"WLFT":-1.2})
        # beam.add_load_combo("COMB31",{"DeadLoad2":1.2,"WLX":1.2})
        # beam.add_load_combo("COMB32",{"DeadLoad2":1.2,"WLFT":1.2})
        # beam.add_load_combo("COMB33",{"DeadLoad2":1.2,"WLX":-1.2})
        # beam.add_load_combo("COMB34",{"DeadLoad2":1.2,"WLFT":-1.2})
        # beam.add_load_combo("COMB35",{"DeadLoad":1.2,"WLX":1.2})
        # beam.add_load_combo("COMB36",{"DeadLoad":1.2,"WLFT":1.2})
        # beam.add_load_combo("COMB37",{"DeadLoad":1.2,"WLX":-1.2})
        # beam.add_load_combo("COMB38",{"DeadLoad":1.2,"WLFT":-1.2})
        # beam.add_load_combo("COMB39",{"DeadLoad2":1.2,"WLX":1.2})
        # beam.add_load_combo("COMB40",{"DeadLoad2":1.2,"WLFT":1.2})
        # beam.add_load_combo("COMB41",{"DeadLoad2":1.2,"WLX":-1.2})
        # beam.add_load_combo("COMB42",{"DeadLoad2":1.2,"WLFT":-1.2})
        # beam.add_load_combo("COMB43",{"DeadLoad":1.2,"EQFT":1.2})
        # beam.add_load_combo("COMB44",{"DeadLoad":1.2,"EQ":1.2})
        # beam.add_load_combo("COMB45",{"DeadLoad":1.2,"EQFT":-1.2})
        # beam.add_load_combo("COMB46",{"DeadLoad":1.2,"EQ":-1.2})
        # beam.add_load_combo("COMB47",{"DeadLoad":1.2,"EQFT":1.2})
        # beam.add_load_combo("COMB48",{"DeadLoad":1.2,"EQ":1.2})
        # beam.add_load_combo("COMB49",{"DeadLoad":1.2,"EQFT":-1.2})
        # beam.add_load_combo("COMB50",{"DeadLoad":1.2,"EQ":-1.2})



        beam.analyze()
        # load_combo = beam.LoadCombos
        # print("load com",len(load_combo))
        # for combo_name in load_combo.keys():
        #     print("Combination Name:", combo_name)
            
           
        # Displaying the JSON format
        # print("data in dict",load_combo)
        # print("\nJSON format = ",type(beam.LoadCombos))
        # col = {}
        # beams = {}
        # level = {}
        # All_Value_Combination = dict()
        
        # All_Value_Combination["col"] = col
        # All_Value_Combination["beam"] = beams
        # All_Value_Combination["col"][combo_name] = {}
        # All_Value_Combination["beam"][combo_name] = {}

        # for comName in load_combo.keys():
        #     print("------>",comName)
        #     md_beam = {}
        #     md_col = {}
        #     x = 6
        #     num_levels = (virticalCounter - colnodecounter2) // x  # Calculate the number of levels

        #     for level in range(1, num_levels + 1):
        #         level_key = "level.{}".format(level)
        #         col_start = 1 + (level - 1) * x
        #         col_end = col_start + x
        #         All_Value_Combination["col"][combo_name][level_key] = {}
                
                
        #         for member in range(col_start,col_end):
        #             member_name = 'M{}'.format(member)
                    
        #             member_deflection_max = beam.Members[member_name].max_deflection('dy', comName)
        #             member_deflection_min = beam.Members[member_name].min_deflection('dy', comName)
                    
        #             location = 0  # Example location along the member's length (0.0 represents the start, 1.0 represents the end)
                    
        #             axial_force_max = beam.Members[member_name].max_axial(comName)
        #             axial_force_min = beam.Members[member_name].min_axial(comName)
                    
        #             member_shear_max = beam.Members[member_name].max_shear('Fy', comName)
        #             member_shear_min = beam.Members[member_name].min_shear('Fy', comName)
                    
        #             member_moment_max = beam.Members[member_name].max_moment('Mz', comName)
        #             member_moment_min = beam.Members[member_name].min_moment('Mz', comName)
                    
        #             #member_moment_maxZ = beam.Members[member_name].max_moment('My', comName)
        #             #member_moment_minZ = beam.Members[member_name].max_torque('Mz', comName)
                    
        #             md_col = {
        #                 # "Deflection_max":member_deflection_max,
        #                 # "Deflection_min":member_deflection_min,
        #                 "Axial_max": axial_force_max,
        #                 # "Axial_min": axial_force_min,
        #                 "Shear_max": member_shear_max,
        #                 "Shear_min": member_shear_min,
        #                 "Moment_max": member_moment_max,
        #                 "Moment_min": member_moment_min,
        #                 # "Moment_maxZ": member_moment_maxZ,
        #                 # "Moment_minZ": member_moment_minZ
        #             }
        #             All_Value_Combination["col"][combo_name][level_key][member_name] = md_col
                
            # for member in range(1,colnodecounter2):
            #     #mD = beam.Members['M{}'.format(member)].max_shear('Fy',comName)
            #     # member_deflection_max =  beam.Members['M{}'.format(member)].max_deflection('dy',comName) #member.max_deflection(combo_name)
            #     # member_deflection_min =  beam.Members['M{}'.format(member)].min_deflection('dy',comName)

            #     # location = 0  # Example location along the member's length (0.0 represents the start, 1.0 represents the end)

            #     axial_force_max = beam.Members['M{}'.format(member)].max_axial(comName)
               

            #     member_shear_max = beam.Members['M{}'.format(member)].max_shear('Fy',comName)
            #     # member_shear_min = beam.Members['M{}'.format(member)].min_shear('Fy',comName)

            #     member_moment_max = beam.Members['M{}'.format(member)].max_moment('Mz',comName)
            #     # member_moment_min = beam.Members['M{}'.format(member)].min_moment('Mz',comName)
                
            #     member_moment_maxZ = beam.Members['M{}'.format(member)].max_moment('My',comName)
            #     member_moment_minZ = beam.Members['M{}'.format(member)].min_moment('Mz',comName)
            #     md_beam['M{}'.format(member)] = {
            #         # "Deflection_max":member_deflection_max,
            #         # "Deflection_min":member_deflection_min,
            #         "Axial_max":axial_force_max,
            #         # "Axial_min":axial_force_min,
            #         "Shear_max":member_shear_max,
            #         # "Shear_min":member_shear_min,
            #         "Moment_max":member_moment_max,
            #         # "Moment_min":member_moment_min,

            #         "Moment_maxZ":member_moment_maxZ,
            #         # "Moment_minZ":member_moment_minZ
            #     } 
            # All_Value_Combination['beams'][comName] =  md_beam
            # no_of_beam = virticalCounter - colnodecounter2
            # print("""""""",type (no_of_beam))
              # Calculate the number of levels

            # x = 6
            # num_levels = (virticalCounter - colnodecounter2) // x  # Calculate the number of levels

            # for level in range(1, num_levels + 1):
            #     level_key = "level.{}".format(level)
            #     col_start = colnodecounter2 + (level - 1) * x
            #     col_end = col_start + x
            #     All_Value_Combination["beam"][combo_name][level_key] = {}
                
                
            #     for member in range(col_start, col_end):
            #         member_name = 'M{}'.format(member)
                    
            #         member_deflection_max = beam.Members[member_name].max_deflection('dy', comName)
            #         member_deflection_min = beam.Members[member_name].min_deflection('dy', comName)
                    
            #         location = 0  # Example location along the member's length (0.0 represents the start, 1.0 represents the end)
                    
            #         axial_force_max = beam.Members[member_name].max_axial(comName)
            #         axial_force_min = beam.Members[member_name].min_axial(comName)
                    
            #         member_shear_max = beam.Members[member_name].max_shear('Fy', comName)
            #         member_shear_min = beam.Members[member_name].min_shear('Fy', comName)
                    
            #         member_moment_max = beam.Members[member_name].max_moment('Mz', comName)
            #         member_moment_min = beam.Members[member_name].min_moment('Mz', comName)
                    
            #         member_moment_maxZ = beam.Members[member_name].max_moment('My', comName)
            #         # member_moment_minZ = beam.Members[member_name].max_torque('Mz', comName)
                    
            #         md_col = {
            #             # "Deflection_max":member_deflection_max,
            #             # "Deflection_min":member_deflection_min,
            #             "Axial_max": axial_force_max,
            #             # "Axial_min": axial_force_min,
            #             "Shear_max": member_shear_max,
            #             # "Shear_min": member_shear_min,
            #             "Moment_max": member_moment_max,
            #             "Moment_min": member_moment_min,
            #             "Moment_maxZ": member_moment_maxZ,
            #             # "Moment_minZ": member_moment_minZ
            #         }
            #         All_Value_Combination["beam"][combo_name][level_key][member_name] = md_col

            # All_Value_Combination["num_levels"] = num_levels

          
            # for member in range(colnodecounter2,virticalCounter):
            #     no_of_beam = virticalCounter - colnodecounter2
            #         #mD = beam.Members['M{}'.format(member)].max_shear('Fy',comName)
            #     member_deflection_max =  beam.Members['M{}'.format(member)].max_deflection('dy',comName) #member.max_deflection(combo_name)
            #     member_deflection_min =  beam.Members['M{}'.format(member)].min_deflection('dy',comName)

            #     location = 0  # Example location along the member's length (0.0 represents the start, 1.0 represents the end)

            #     axial_force_max = beam.Members['M{}'.format(member)].max_axial(comName)
            #     axial_force_min =  beam.Members['M{}'.format(member)].min_axial(comName)

            #     member_shear_max = beam.Members['M{}'.format(member)].max_shear('Fy',comName)
            #     member_shear_min = beam.Members['M{}'.format(member)].min_shear('Fy',comName)

            #     member_moment_max = beam.Members['M{}'.format(member)].max_moment('Mz',comName)
            #     member_moment_min = beam.Members['M{}'.format(member)].min_moment('Mz',comName)
                
            #     member_moment_maxZ = beam.Members['M{}'.format(member)].max_moment('My',comName)
            #     # member_moment_minZ = beam.Members['M{}'.format(member)].max_torque('Mz',comName)
            #     md_col['M{}'.format(member)] = {
            #         # "Deflection_max":member_deflection_max,
            #         # "Deflection_min":member_deflection_min,
            #         "Axial_max":axial_force_max,
            #         # "Axial_min":axial_force_min,
            #         "Shear_max":member_shear_max,
            #         # "Shear_min":member_shear_min,
            #         "Moment_max":member_moment_max,
            #         # "Moment_min":member_moment_min,

            #         "Moment_maxZ":member_moment_maxZ,
            #         "Moment_minZ":member_moment_minZ
            #     } 
            # All_Value_Combination["level{}".format(i)]['col'][comName] =  md_col
        



#         import json 
# # Serializing json  
#         json_object = json.dumps(All_Value_Combination) 
#         # print(json_object) 
#         with open("sample.json", "w") as outfile:
#             json.dump(All_Value_Combination, outfile)    
#         # print("WHole value",All_Value_Combination)       
#         Max_mom = get_maximum_moments(All_Value_Combination)
#         print("------------------->>>>>>",Max_mom)
        
        
        # moment = 5.00 
        # depth_of_beam = 650.00
        # eff_depth = 600
        # sigst = 130 
        # max_area = calculate_area(Max_mom,sigst,eff_depth,depth_of_beam)
        # result = beamdesign(moment,sigst,eff_depth,depth_of_beam)
        # print("=======================> area of steel",result)
        # print("+++++++++++++>",max_area)
        # beam.Members['M42'].plot_moment(Direction='My',combo_name='COMB1')
        # beam.Members['M42'].plot_moment(Direction='Mz',combo_name="COMB1")
        

        # Input parameters
        # fc = 25  # Concrete compressive strength (MPa)
        # fy = 500  # Steel yield strength (MPa)
        # b = 300  # Width of the column (mm)
        # d = 600  # Effective depth of the column (mm)
        # moments = np.array([100, 200, 300, 400, 500])  # Moments (kNm)

        # # Generate interaction curve and calculate required area of steel
        # required_area = pmm_interaction_curve(fc, fy, b, d, moments)
        # print("required arry__________________________________",required_area)
        # plt.show()
                    
        # print("ALL valie",member_results)        
        # print('Maximum Shear:', beam.Members['M1'].max_shear('Fy', 'DeadLoad1'), 'kip')
        # print('Minimum Shear:', beam.Members['M1'].min_shear('Fy', 'DeadLoad1'), 'kip')
        # print('Maximum Moment:',beam.Members['M1'].max_moment('Mz', 'DeadLoad1')/12, 'kip-ft')
        # print('Minimum Moment:',beam.Members['M1'].min_moment('Mz', 'DeadLoad1')/12, 'kip-ft')

        # # Print the max/min deflections in the beam
        # print('Maximum Deflection:', beam.Members['M1'].max_deflection('dy', 'DeadLoad1'), 'in')
        # print('Minimum Deflection:', beam.Members['M1'].min_deflection('dy', 'DeadLoad1'), 'in')
        # Print the shear, moment, and deflection diagrams
       # beam.Members['M1'].plot_shear('Fy')
       # beam.Members['M1'].plot_moment('Mz')
       # beam.Members['M1'].plot_deflection('dy')

        # Print reactions at each end of the beam
        # print('Left Support Reaction:1', beam.Nodes['N1'].RxnFY, 'kip')
        # print('Right Support Reacton:2', beam.Nodes['N2'].RxnFY, 'kip')
        # print('Node 3',beam.Nodes['N3'].RxnFY,'kip')
        # print('Node 4',beam.Nodes['N3'].RxnFY,'kip')
        # print('Node 5',beam.Nodes['N3'].RxnFY,'kip')
        # print("Node 6",beam.Nodes['N6'].RxnFY)
        #print('Node 6',beam.Deflections["S1"]
        #print("S1 node deflection",beam.Nodes['S1'].RxnFY,"kip")

        #print('N1 displacement in Y =', beam.Nodes['S1'].DY)

       # node_deflection = beam.Nodes["S1"].Translation

        # Print the deflection
        # print("Deflection at node S1: ", node_deflection)

        # Render the deformed shape of the beam magnified 100 times, with a text
        # height of 5 inches
        from PyNite.Visualization import Renderer
        renderer = Renderer(beam)
        renderer.annotation_size = 2
        renderer.deformed_shape = False
        renderer.deformed_scale = 1
        renderer.render_loads = True
        # renderer.labels= False
        # renderer.case='SC'
        # renderer.combo_name = 'COMB1'
        renderer.render_model()




    # Render the form
    return '''
        <form method="post">
            <label for="numberofcol">Number Of Col:</label>
            <input type="number" name="numberofcol" id="numberofcol" required><br><br>

            <label for="stgh">stgh:</label>
            <input type="number" name="stgh" id="stgh" required><br><br>

            <label for="nooftybeams">No of tybeams:</label>
            <input type="number" name="nooftybeams" id="nooftybeams" required><br><br>

            <label for="foundationdepth">Foundation of depth:</label>
            <input type="number" name="foundationdepth" id="foundationdepth" required><br><br>
        
            <label for="coloumtocolum">Coloum To Coloum:</label>
            <input type="number" name="coloumtocolum" id="coloumtocolum+" required><br><br>

            <label for="coloumsize>Coloum Size</label>
            <input type="number" name="coloumsize" id="coloumsize" required><br><br>



            <button type="submit">Generate DXF File</button>
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)