import numpy as np

def material_matrix(E, nu):
    """
    Plane stress material matrix.
    """

    D = (E / (1 - nu**2)) * np.array([[1, nu, 0],
                                      [nu, 1, 0],
                                      [0, 0, (1 - nu) / 2]])

    return D


def element_stiffness(coords, E, nu, thickness):
    """
    Calculate stiffness matrix for a
    3-node constant-strain triangular element.

    coords:
        [[x1, y1],
         [x2, y2],
         [x3, y3]]
    """

    x1, y1 = coords[0]
    x2, y2 = coords[1]
    x3, y3 = coords[2]

    # Element area
    area = 0.5 * abs(
        x1 * (y2 - y3)
        + x2 * (y3 - y1)
        + x3 * (y1 - y2)
    )

    if area <= 0:
        raise ValueError("Element has zero area.")


    # b and c coefficients
    b1 = y2 - y3
    b2 = y3 - y1
    b3 = y1 - y2

    c1 = x3 - x2
    c2 = x1 - x3
    c3 = x2 - x1


    # Strain-displacement matrix B
    B = (1 / (2 * area)) * np.array([
        [b1, 0, b2, 0, b3, 0],
        [0, c1, 0, c2, 0, c3],
        [c1, b1, c2, b2, c3, b3]
    ])


    # Material matrix
    D = material_matrix(E, nu)

    # Element stiffness matrix
    Ke = thickness * area * (B.T @ D @ B)

    return Ke


def assemble_global_stiffness(nodes, elements, E, nu, thickness):
    """
    Assemble all element stiffness matrices
    into the global stiffness matrix.
    """

    n_nodes = len(nodes)

    # 2 DOF per node: ux and uy
    n_dof = 2 * n_nodes

    K = np.zeros((n_dof, n_dof))

    for element in elements:

        # Node IDs
        n1, n2, n3 = element

        # Element coordinates
        coords = nodes[[n1, n2, n3]]

        # Element stiffness
        Ke = element_stiffness(coords, E, nu, thickness)

        # Global DOF mapping
        dofs = [2 * n1, 2 * n1 + 1, 2 * n2, 2 * n2 + 1, 2 * n3, 2 * n3 + 1]


        # Assembly
        for i in range(6):
            for j in range(6):
                K[dofs[i], dofs[j]] += Ke[i, j]

    return K