import numpy as np
def generate_mesh(L, H, nx, ny):
    """
    Generate a structured rectangular mesh
    and divide each rectangle into two triangles.

    Parameters
    ----------
    L : Beam length.
    H : Beam height.
    nx : Number of divisions along length.
    ny : Number of divisions along height.

    Returns
    -------
    nodes : ndarray
        Node coordinates, shape (n_nodes, 2)
    elements : ndarray
        Triangle connectivity, shape (n_elements, 3)
    """

    # Generate nodes
    x = np.linspace(0, L, nx + 1)
    y = np.linspace(0, H, ny + 1)

    nodes = []

    for j in range(ny + 1):
        for i in range(nx + 1):
            nodes.append([x[i], y[j]])

    nodes = np.array(nodes, dtype=float)

    # Generate triangular elements
    elements = []

    for j in range(ny):
        for i in range(nx):

            # Node numbering
            n1 = j * (nx + 1) + i
            n2 = n1 + 1
            n3 = n1 + (nx + 1)
            n4 = n3 + 1

            # Divide rectangle into two triangles
            elements.append([n1, n2, n4])
            elements.append([n1, n4, n3])

    elements = np.array(elements, dtype=int)

    return nodes, elements