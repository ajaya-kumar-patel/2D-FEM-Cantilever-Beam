import time
import numpy as np

from mesh import generate_mesh
from fem import assemble_global_stiffness
from boundary_conditions import (
    get_fixed_dofs,
    apply_load
)
from solver import solve_system



# Problem parameters
L = 10.0
H = 2.0

E = 200e9
nu = 0.30

thickness = 0.1
load = 1000.0


# Different mesh resolutions
mesh_sizes = [5, 10, 20, 30, 40]


results = []



# Mesh refinement experiment
for nx in mesh_sizes:
    # Keep aspect ratio approximately constant
    ny = max(2, nx // 5)

    start_time = time.perf_counter()

    # Generate mesh
    nodes, elements = generate_mesh(L, H, nx, ny)

    # Assemble stiffness matrix
    K = assemble_global_stiffness(nodes, elements, E, nu, thickness)

    # Boundary conditions
    fixed_dofs = get_fixed_dofs(nodes)

    F, load_node = apply_load(nodes, load)

    # Solve
    U = solve_system(K, F, fixed_dofs)

    elapsed = time.perf_counter() - start_time

    # Displacement at loaded node
    tip_ux = U[2 * load_node]
    tip_uy = U[2 * load_node + 1]

    tip_magnitude = np.sqrt(tip_ux**2 + tip_uy**2)

    # Store result

    results.append([nx, ny, len(nodes), len(elements), tip_uy, tip_magnitude, elapsed])



# Print results
print("\nMesh Refinement Results")
print("-" * 80)

print(
    f"{'nx':>5}"
    f"{'ny':>5}"
    f"{'Nodes':>10}"
    f"{'Elements':>12}"
    f"{'Tip Uy':>15}"
    f"{'Runtime':>15}"
)

print("-" * 80)

for result in results:
    nx, ny, nodes_n, elements_n, uy, mag, runtime = result
    print(
        f"{nx:>5}"
        f"{ny:>5}"
        f"{nodes_n:>10}"
        f"{elements_n:>12}"
        f"{uy:>15.6e}"
        f"{runtime:>15.6f}"
    )



# Plot convergence
import matplotlib.pyplot as plt
elements_count = [r[3] for r in results]

tip_displacements = [abs(r[4]) for r in results]

runtimes = [r[6] for r in results]


# Displacement vs elements
plt.figure(figsize=(8, 5))
plt.plot(elements_count, tip_displacements, marker="o")
plt.xlabel("Number of Elements")
plt.ylabel("Absolute Tip Displacement (m)")
plt.title("Mesh Refinement vs Tip Displacement")
plt.grid(True)

plt.savefig("results/convergence.png", dpi=300, bbox_inches="tight")
plt.show()


# Runtime vs elements
plt.figure(figsize=(8, 5))
plt.plot(elements_count, runtimes, marker="o")
plt.xlabel("Number of Elements")
plt.ylabel("Runtime (seconds)")
plt.title("Mesh Refinement vs Computational Cost")
plt.grid(True)

plt.savefig("results/runtime.png", dpi=300, bbox_inches="tight")
plt.show()