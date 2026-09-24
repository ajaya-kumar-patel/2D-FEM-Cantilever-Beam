import numpy as np

def get_fixed_dofs(nodes, tolerance=1e-10):
    """
    Fix all DOFs of nodes located at x = 0.
    """

    fixed_dofs = []

    for node_id, (x, y) in enumerate(nodes):

        if abs(x) < tolerance:

            # x displacement DOF
            fixed_dofs.append(2 * node_id)

            # y displacement DOF
            fixed_dofs.append(2 * node_id + 1)

    return np.array(fixed_dofs, dtype=int)


def apply_load(nodes, total_load):
    """
    Apply downward point load at the top-right node.
    """

    n_nodes = len(nodes)

    F = np.zeros(2 * n_nodes)

    # Find nodes at maximum x
    max_x = np.max(nodes[:, 0])

    right_nodes = np.where(
        np.isclose(nodes[:, 0], max_x)
    )[0]

    # Choose the top-right node
    top_right_node = right_nodes[
        np.argmax(nodes[right_nodes, 1])
    ]

    # Apply downward load in y direction
    F[2 * top_right_node + 1] = -total_load

    return F, top_right_node