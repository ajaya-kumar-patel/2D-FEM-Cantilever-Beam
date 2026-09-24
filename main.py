import os
import numpy as np

from mesh import generate_mesh
from fem import assemble_global_stiffness
from boundary_conditions import (
    get_fixed_dofs,
    apply_load
)
from solver import solve_system
from visualization import (
    plot_mesh,
    plot_deformation
)



# 1. Problem definition

L = 10.0              # Length (m)
H = 2.0               # Height (m)

E = 200e9             # Young's modulus (Pa)
nu = 0.30             # Poisson's ratio

thickness = 0.1       # Thickness (m)

load = 1000.0         # Downward load (N)

nx = 20               # Number of divisions in x
ny = 4                # Number of divisions in y



# 2. Create results directory
os.makedirs("results", exist_ok=True)


# 3. Generate mesh
nodes, elements = generate_mesh(L, H, nx, ny)

print("Number of nodes:", len(nodes))
print("Number of elements:", len(elements))



# 4. Plot mesh
plot_mesh(nodes, elements, "results/mesh.png")

# 5. Assemble global stiffness matrix
K = assemble_global_stiffness(nodes, elements, E, nu, thickness)

print("Global stiffness matrix shape:", K.shape)


# 6. Apply boundary conditions
fixed_dofs = get_fixed_dofs(nodes)

F, load_node = apply_load(nodes, load)

print("Load applied at node:", load_node)
print("Fixed DOFs:", len(fixed_dofs))


# 7. Solve KU = F
U = solve_system(K, F, fixed_dofs)

# 8. Extract displacement information
displacements = U.reshape(-1, 2)

magnitudes = np.linalg.norm(displacements, axis=1)

max_displacement = np.max(magnitudes)

print("Maximum displacement:", max_displacement, "m")

# 9. Plot deformation
plot_deformation(nodes, elements, U, scale=100, filename="results/deformation.png")