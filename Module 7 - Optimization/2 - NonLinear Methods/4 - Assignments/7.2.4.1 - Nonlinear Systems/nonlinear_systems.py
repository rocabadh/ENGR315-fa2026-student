"""ENGR 315 | Nonlinear Systems Assignment

Complete the four functions below. Do not change their names, parameters,
or return types. Submit this file to Gradescope.

You may use NumPy and SciPy. Do not hard-code the final dimensions.
"""
import numpy as np
from scipy.optimize import root


def residuals(dimensions):
    """Return a NumPy array of shape (2,) with [f1, f2].

    f1(x, y) = x**2 + y**2 - 41
    f2(x, y) = x + y - 9
    """
    # TODO (20 points): implement the nonlinear equations.
    x,y =dimensions
    f1=(x**2)+(y**2)-41
    f2=x+y-9
    return np.array([f1,f2], dtype=float)


def jacobian(dimensions):
    """Return a NumPy array of shape (2, 2) containing the Jacobian."""
    # TODO (20 points): implement the Jacobian matrix.
    x,y=dimensions
    return np.array([[2*x,2*y],[1,1]], dtype=float)


def newton_raphson(initial_guess, tolerance=1e-6, max_iterations=50):
    """Return a NumPy array of shape (2,) with the converged dimensions.

    Use a for loop and np.linalg.solve(J, -F). Stop when the maximum
    absolute residual is strictly smaller than tolerance. If the solver
    does not converge within max_iterations, raise RuntimeError.
    """
    # TODO (40 points): implement the iterative Newton-Raphson algorithm.
    current=np.array(initial_guess, dtype=float)
    for _ in range(max_iterations):
        f=residuals(current)
        if np.max(np.abs(f))<tolerance:
            return current 
        j=jacobian(current)
        delta=np.linalg.solve(j,-f)
        current = current+delta
    if np.max(np.abs(residuals(current)))<tolerance:
        return current
    raise RuntimeError(f"Newton-Raphson did not converge within {max_iterations} iterations.")
    


def solve_scipy(initial_guess):
    """Return a NumPy array of shape (2,) using scipy.optimize.root.

    Check solution.success. Raise RuntimeError if the solver fails.
    """
    # TODO (20 points): use root() to solve the system.
    solution=root(residuals, initial_guess)
    if not solution.success:
        raise RuntimeError(f"SciPy Solver Failed: {solution.message}")
    return np.asarray(solution.x, dtype=float)


if __name__ == "__main__":
    guess = np.array([3.0, 6.0])
    print("Initial guess:", guess)
    print("Residuals at guess:", residuals(guess))
    print("Jacobian at guess:\n", jacobian(guess))
    print("NumPy Newton-Raphson:", newton_raphson(guess))
    print("SciPy root:", solve_scipy(guess))
