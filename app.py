from flask import Flask, request, send_file
from PyNite import FEModel3D
import ezdxf
import math
import PyNite


app = Flask(__name__)

@app.route('/check',methods=['GET','POST'])
def check():
    if request.method == 'GET':
        return "run"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        
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
#  #     # Define a material
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
    #     beam.analyze()


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
        beam = FEModel3D()
        radius = 48
        dx = 60
        num_tie = 8
        st = 350
        num_cols =  8
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
        for k in range(num_tie +1):
            for m in range(num_cols):
                angle = m* (2*math.pi/num_cols)
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                beam.add_node(f'N{nodeCounter+1}', x, y, dx+ (k+1)*st/(num_tie+1))
                nodeCounter = nodeCounter +1 
        print("nodeCounter",nodeCounter)
        checkNode = beam.Nodes['N1']

        print('Node properties:')
        print('X:', checkNode.X)
        print('Y:', checkNode.Y)
        print('Z:', checkNode.Z)
        for z in range(nodeCounter):
            check = 'N{}'.format(z+1)
            temp =beam.Nodes[check]
            print("coodinate of each nodeX:",check ,temp.X)
            print("coodinate of each nodeY:",check, temp.Y)
            print("coodinate of each nodeZ:",check,temp.Z)
        # Add nodes (14 ft = 168 inches apart)
       # beam.add_node('N1', 0, 0, 0)
       # beam.add_node('N2', 168, 0, 0)

       # Define a material
        E =  0.00315 #29000       # Modulus of elasticity (ksi)
        G =   0.00134   #11200       # Shear modulus of elasticity (ksi)
        nu =  0.17 #0.3        # Poisson's ratio
        rho = 0.654302 # 2.836e-4  # Density (kci)
        beam.add_material('Steel', E, G, nu, rho)
        dbw2 = 300

        # Add a beam with the following properties:
        # Iy = 100 in^4, Iz = 150 in^4, J = 250 in^4, A = 20 in^2
        #beam.add_member('M1', 'N1', 'N2', 'Steel', 100, 150, 250, 20)
        #print(PyNite.__version__)
        offset_start = [0, 0, 10]  # [x, y, z] offset at the start of the member
        offset_end = [0, 0, -10] 


        number_of_col = (num_tie+2)*num_cols 
        counterNumberofCol = 0
        for l in range(number_of_col):
            print("printl ",l)
            print("meamber Name",l+1)
            print("first target",l+1)
            print("second target node",l+num_cols+1)

            beam.add_member('M{}'.format(l+1),'N{}'.format(l+1),'N{}'.format(l+num_cols+1),'Steel',100,150,250,20)
            counterNumberofCol = counterNumberofCol+1

        print("number vertical col ", counterNumberofCol)




        counterNumberofCol = counterNumberofCol+1

        # add horizontal memebers 
        #virticalCounter = 0
        for m  in range(1,num_tie+2):
            for p in range(1,num_cols+1):
                if p == num_cols:
                    beam.add_member('M{}'.format(counterNumberofCol),'N{}'.format(num_cols+p+(m-1)*num_cols),'N{}'.format(num_cols+1+p+(m-2)*num_cols),"Steel",100, 150, 250, 20)
                  #  virticalCounter = verticalCounter+1
                    counterNumberofCol = counterNumberofCol +1
                else:
                    extra1 = num_cols+p+(m-1)*num_cols
                    extra2 = num_cols+1+p+(m-1)*num_cols
                    print('nodes 1',extra1)
                    print('nodes 2 ',extra2)
                    beam.add_member('M{}'.format(counterNumberofCol),'N{}'.format(num_cols+p+(m-1)*num_cols),'N{}'.format(num_cols+1+p+(m-1)*num_cols),"Steel",100, 150, 250, 20)
                   # virticalCounter = virticalCounter+1
                    counterNumberofCol = counterNumberofCol +1 

        #print("horizontal",virticalCounter)    


        
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
        # beam.add_member_dist_load('M1', 'Fy', 200/1000/12, 200/1000/12)
        beam.add_node("S1",0,0,st+dx)
        for i in range(num_cols):
            beam.add_member("H{}".format(i+10),"S1",'N{}'.format(nodeCounter),"Steel",100, 150, 250, 20)
            nodeCounter = nodeCounter-1
        beam.add_node_load("S1","FY",1)       # Analyze the beam
        beam.analyze()

        # Print the shear, moment, and deflection diagrams
        beam.Members['M1'].plot_shear('Fy')
        beam.Members['M1'].plot_moment('Mz')
        beam.Members['M1'].plot_deflection('dy')

        # Print reactions at each end of the beam
        print('Left Support Reaction:1', beam.Nodes['N1'].RxnFY, 'kip')
        print('Right Support Reacton:2', beam.Nodes['N2'].RxnFY, 'kip')
        print('Node 3',beam.Nodes['N3'].RxnFY,'kip')
        print('Node 4',beam.Nodes['N3'].RxnFY,'kip')
        print('Node 5',beam.Nodes['N3'].RxnFY,'kip')
        print('Node 6',beam.Nodes['N3'].RxnFY,'kip')
        print("S1 node deflection",beam.Nodes['S1'].RxnFY,"kip")

        # Render the deformed shape of the beam magnified 100 times, with a text
        # height of 5 inches
        from PyNite.Visualization import Renderer
        renderer = Renderer(beam)
        renderer.annotation_size = 6
        renderer.deformed_shape = True
        renderer.deformed_scale = 1
        renderer.render_loads = True
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