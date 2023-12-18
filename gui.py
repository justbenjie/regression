import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from regression import Regression
from file_handling import FileHandler


class PolynomialRegressionGUI:
    def __init__(self):
        self.x = None
        self.y = None
        self.coefficients = None

        self.window = tk.Tk()
        self.window.title("Polynomial Regression")
        self.window.geometry("800x900")

        self.top_frame = tk.Frame(self.window)
        self.top_frame.pack(pady=20)

        self.load_button = tk.Button(
            self.top_frame,
            text="Load Data",
            command=self.load_data_and_plot,
            font=("Arial", 11),
        )
        self.load_button.pack(side=tk.LEFT, padx=10)

        self.degree_label = tk.Label(
            self.top_frame, text="Polynomial Degree (1-6):", font=("Arial", 11)
        )
        self.degree_label.pack(side=tk.LEFT)
        self.degree_entry = tk.Entry(self.top_frame, font=("Arial", 11), width=5)
        self.degree_entry.pack(side=tk.LEFT)

        self.plot_button = tk.Button(
            self.top_frame,
            text="Plot",
            command=self.plot_loaded_data,
            font=("Arial", 11),
        )
        self.plot_button.pack(side=tk.LEFT, padx=10)

        self.chart_frame = tk.Frame(self.window)
        self.chart_frame.pack(pady=20)

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack()

        self.equation_label = tk.Label(
            self.window, text="Regression Equation: ", font=("Arial", 11)
        )
        self.equation_label.pack(pady=10)

        self.calc_y_frame = tk.Frame(self.window)
        self.calc_y_frame.pack(pady=20)

        self.calc_y_label = tk.Label(
            self.calc_y_frame, text="Calculate y for x:", font=("Arial", 11)
        )
        self.calc_y_label.pack(side=tk.LEFT)
        self.calc_y_entry = tk.Entry(self.calc_y_frame, font=("Arial", 11), width=10)
        self.calc_y_entry.pack(side=tk.LEFT)
        self.calc_y_button = tk.Button(
            self.calc_y_frame,
            text="Calculate",
            command=self.calculate_y,
            font=("Arial", 11),
        )
        self.calc_y_button.pack(side=tk.LEFT, padx=10)
        self.calc_y_result_label = tk.Label(
            self.calc_y_frame, text="", font=("Arial", 11)
        )
        self.calc_y_result_label.pack(side=tk.LEFT)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit the program?"):
            self.window.destroy()
            exit()

    def load_data_and_plot(self):
        file_handler = FileHandler()
        self.x, self.y = file_handler.load_data()
        if self.x is not None and self.y is not None:
            messagebox.showinfo("Success", "Data loaded successfully.")

    def plot_loaded_data(self):
        degree_text = self.degree_entry.get()
        if degree_text.isdigit():
            degree = int(degree_text)
            if 1 <= degree <= 6:
                if self.x is not None and self.y is not None:
                    plotter = Regression()
                    self.coefficients = plotter.least_squares(self.x, self.y, degree)
                    fig, ax = plotter.plot_regression(self.x, self.y, degree)
                    self.canvas.figure = fig
                    self.canvas.draw()
                    self.equation_label.config(
                        text="Regression Equation: " + self.get_equation_text()
                    )
                else:
                    messagebox.showerror(
                        "Error", "No data is loaded. Please load data before plotting."
                    )
            else:
                messagebox.showerror("Error", "Degree should be between 1 and 6.")
        else:
            messagebox.showerror("Error", "Degree should be a positive integer.")

    def get_equation_text(self):
        degree = int(self.degree_entry.get())
        if self.coefficients is not None:
            equation = "y = "
            for i, coeff in enumerate(self.coefficients[::1]):
                power = degree - i  # Calculate the power for the term
                equation += f"{coeff:.2f}x^{power} + "
            equation = equation[:-3]  # Remove the trailing "+"
            return equation
        else:
            return "No regression equation available. Please plot data first."

    def calculate_y(self):
        x_text = self.calc_y_entry.get()
        if x_text:
            if self.coefficients is not None:
                try:
                    x = float(x_text)
                    y = self.evaluate_polynomial(x)
                    self.calc_y_result_label.config(text=f"y = {y:.3f}")
                except ValueError:
                    messagebox.showerror("Error", "Invalid input for x.")
            else:
                messagebox.showerror(
                    "Error", "No regression equation available. Please plot data first."
                )
        else:
            messagebox.showerror("Error", "Please enter a value for x.")

    def evaluate_polynomial(self, x):
        result = 0
        for i, coefficient in enumerate(self.coefficients[::-1]):
            result += coefficient * (x**i)
        return result
