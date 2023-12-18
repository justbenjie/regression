import numpy as np
import matplotlib.pyplot as plt


class Regression:
    def plot_regression(self, x, y, degree):
        coefficients = self.least_squares(x, y, degree)

        x_range = np.linspace(min(x), max(x), 100)
        X_range = np.vander(x_range, degree + 1)
        y_range = np.dot(X_range, coefficients)

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        ax.scatter(x, y, label="Data")
        ax.plot(x_range, y_range, color="red", label="Polynomial Regression")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Polynomial Regression using Least Squares")
        ax.legend()

        return fig, ax

    # def least_squares(self, x, y, degree):
    #     X = np.vander(x, degree + 1)
    #     XtX = np.dot(X.T, X)
    #     Xty = np.dot(X.T, y)
    #     coefficients = np.linalg.solve(XtX, Xty)
    #     return coefficients

    def least_squares(self, x, y, degree):
        n = len(x)
        m = degree + 1

        # Initialize the X matrix
        X = [[0] * m for _ in range(n)]

        # Populate the X matrix
        for i in range(n):
            for j in range(m):
                X[i][j] = x[i] ** j

        # Calculate XtX
        XtX = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                for k in range(n):
                    XtX[i][j] += X[k][i] * X[k][j]

        # Calculate Xty
        Xty = [0] * m
        for i in range(m):
            for j in range(n):
                Xty[i] += X[j][i] * y[j]

        # Solve for coefficients
        coefficients = self.solve_system(XtX, Xty)

        return coefficients

    def solve_system(self, A, b):
        n = len(A)

        # Forward elimination
        for i in range(n):
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]

        # Back substitution
        x = [0] * n
        for i in range(n - 1, -1, -1):
            for j in range(i + 1, n):
                b[i] -= A[i][j] * x[j]
            x[i] = b[i] / A[i][i]

        return x
