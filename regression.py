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

    def least_squares(self, x, y, degree):
        X = np.vander(x, degree + 1)
        XtX = np.dot(X.T, X)
        Xty = np.dot(X.T, y)
        coefficients = np.linalg.solve(XtX, Xty)
        return coefficients
