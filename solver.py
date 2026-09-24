import numpy as np

def solve_system(K, F, fixed_dofs):
    """
    Solve KU = F with prescribed zero displacement
    boundary conditions.
    """

    n_dof = len(F)

    all_dofs = np.arange(n_dof)

    # Free DOFs
    free_dofs = np.setdiff1d(
        all_dofs,
        fixed_dofs
    )

    # Reduced system
    K_free = K[np.ix_(free_dofs, free_dofs)]
    F_free = F[free_dofs]

    # Solve
    U_free = np.linalg.solve(
        K_free,
        F_free
    )

    # Full displacement vector
    U = np.zeros(n_dof)

    U[free_dofs] = U_free

    return U