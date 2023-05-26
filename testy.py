from pynite import FEModel3D
import numpy as np

# Define the properties of the beam
E = 29e6  # Modulus of elasticity (psi)
G = 11.5e6  # Shear modulus (psi)
I = 100  # Moment of inertia (in^4)
A = 10  # Cross-sectional area (in^2)
L = 120  # Length of the beam (in)

# Define the nodes of the beam
nodes = []
nodes.append((0, 0))
nodes.append((0, L))

# Define the elements of the beam
elements = []
elements.append((0, 1))

# Create the finite element model
model = FEModel3D()

# Add nodes to the model
for node in nodes:
    model.add_node(node[0], node[1], 0)

# Add elements to the model
for element in elements:
    model.add_member(element[0], element[1], E=E, G=G, Ix=I, A=A)

# Add infinite elements to the model
for node in nodes:
    model.add_infinite_support(node[0], node[1], stiffness='elastic')

# Add point loads to the model
model.add_node_load(0, 'fy', -100)

# Solve the model
model.solve()

# Print the deflection at the tip of the beam
print(f"Deflection at the tip of the beam: {model.get_node_displacement(1, 'y'):.4f} in")