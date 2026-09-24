import numpy as np
import matplotlib.pyplot as plt

def plot_mesh(nodes, elements, filename=None):
    """
    Plot the undeformed triangular mesh.
    """

    plt.figure(figsize=(10, 4))

    for element in elements:

        points = nodes[element]

        # Close the triangle
        points = np.vstack([points, points[0]])

        plt.plot(points[:, 0], points[:, 1], linewidth=0.8)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Undeformed FEM Mesh")
    plt.axis("equal")
    plt.grid(True)

    if filename:
        plt.savefig(filename, dpi=300, bbox_inches="tight")

    plt.show()


def plot_deformation(nodes, elements, U, scale=100, filename=None):
    """
    Plot original and deformed mesh.
    """

    # Convert displacement vector into (n_nodes, 2)
    displacements = U.reshape(-1, 2)

    # Scaled deformation for visualization
    deformed_nodes = (nodes + scale * displacements)

    plt.figure(figsize=(10, 4))

    # Original mesh
    for element in elements:
        points = nodes[element]
        points = np.vstack([points, points[0]])

        plt.plot(points[:, 0], points[:, 1], linestyle="--", linewidth=0.7, alpha=0.5)


    # Deformed mesh
    for element in elements:
        points = deformed_nodes[element]
        points = np.vstack([points, points[0]])

        plt.plot(points[:, 0], points[:, 1], linewidth=1.0)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"Deformed Cantilever Beam (scale = {scale}x)")

    plt.axis("equal")
    plt.grid(True)

    if filename:
        plt.savefig(filename, dpi=300, bbox_inches="tight")

    plt.show()