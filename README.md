# 2D FEM Analysis of a Cantilever Beam

A simple 2D Finite Element Method (FEM) implementation in Python for analyzing the deformation of a cantilever beam under an applied load.

The project implements the main FEM steps from scratch using NumPy, including mesh generation, element stiffness calculation, global stiffness matrix assembly, boundary-condition handling, and nodal displacement computation.

## Methodology

The beam is modeled using a 2D plane-stress FEM formulation with 3-node Constant Strain Triangular (CST) elements.

The implementation follows these steps:

1. Generate a structured triangular mesh.
2. Calculate the stiffness matrix for each element.
3. Assemble element matrices into the global stiffness matrix.
4. Apply boundary conditions and external loading.
5. Solve the resulting linear system for nodal displacements.
6. Visualize the undeformed and deformed mesh.

The FEM system is formulated as:

$$
KU = F
$$

where:

- $K$ = Global stiffness matrix
- $U$ = Nodal displacement vector
- $F$ = Global force vector

## Mesh Refinement Study

The solver was tested with progressively finer meshes to study convergence and computational cost.

| nx | ny | Nodes | Elements | Tip Uy (m) |
|---:|---:|------:|---------:|-----------:|
| 5  | 2 | 18  | 20  | -9.70e-06 |
| 10 | 2 | 33  | 40  | -1.40e-05 |
| 20 | 4 | 105 | 160 | -2.12e-05 |
| 30 | 6 | 217 | 360 | -2.35e-05 |
| 40 | 8 | 369 | 640 | -2.45e-05 |

The tip displacement approaches a stable value as the mesh is refined, while computational cost increases with mesh size.

## Analytical Validation

The FEM result was compared with the Euler-Bernoulli beam solution:

$$
\delta = \frac{PL^3}{3EI}
$$

For the given beam parameters, the analytical tip displacement is approximately:

$$
2.50 \times 10^{-5}\ \text{m}
$$

The finest FEM mesh gives approximately:

$$
2.45 \times 10^{-5}\ \text{m}
$$

The close agreement provides a basic validation of the implementation.

## Project Structure

```text
2D-FEM-Cantilever-Beam/
│
├── main.py
├── mesh.py
├── fem.py
├── boundary_conditions.py
├── solver.py
├── visualization.py
├── mesh_refinement.py
├── requirements.txt
│
└── results/
    ├── mesh.png
    ├── deformation.png
    ├── convergence.png
    └── runtime.png