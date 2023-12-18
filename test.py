import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


def load_data():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        try:
            data = pd.read_excel(file_path)
            x = data["x"].values
            y = data["y"].values
            return x, y
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while loading the data: {str(e)}"
            )
    return None, None


def least_squares(x, y, degree):
    X = np.vander(x, degree + 1)
    XtX = np.dot(X.T, X)
    Xty = np.dot(X.T, y)
    coefficients = np.linalg.solve(XtX, Xty)
    return coefficients


def plot_regression(x, y, degree):
    coefficients = least_squares(x, y, degree)

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

    equation = "Regression Equation: "
    for i, coeff in enumerate(coefficients[::1]):
        power = degree - i  # Calculate the power for the term
        equation += f"{coeff:.2f}x^{power} + "
    equation = equation[:-3]  # Remove the trailing "+"
    equation_label.config(text=equation)  # Update the equation label

    return fig, ax


def load_data_and_plot():
    global x, y
    x, y = load_data()
    if x is not None and y is not None:
        messagebox.showinfo("Success", "Data loaded successfully.")


def plot_loaded_data():
    degree_text = degree_entry.get()
    if degree_text.isdigit():
        degree = int(degree_text)
        if 1 <= degree <= 6:
            if x is not None and y is not None:
                fig, ax = plot_regression(x, y, degree)
                canvas.figure = fig
                canvas.draw()
            else:
                messagebox.showerror(
                    "Error", "No data is loaded. Please load data before plotting."
                )
        else:
            messagebox.showerror("Error", "Degree should be between 1 and 6.")
    else:
        messagebox.showerror("Error", "Degree should be a positive integer.")


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit the program?"):
        window.destroy()
        exit()


def get_custom_y():
    custom_x = custom_x_entry.get()

    if custom_x.isdigit():
        custom_x = float(custom_x)
        if x is not None and y is not None:
            degree_text = degree_entry.get()
            if degree_text.isdigit() and 1 <= int(degree_text) <= 6:
                degree = int(degree_text)
                coefficients = least_squares(x, y, degree)
                custom_y = evaluate_regression(custom_x, coefficients)
                custom_y_label.config(text=f"Custom Y: {custom_y:.2f}")
            else:
                messagebox.showerror("Error", "Degree should be between 1 and 6.")
        else:
            messagebox.showerror(
                "Error",
                "No data is loaded. Please load data before getting the custom Y value.",
            )
    else:
        messagebox.showerror("Error", "Custom X should be a number.")


def evaluate_regression(x, coefficients):
    y = np.polyval(coefficients[::1], x)
    return y


x = None
y = None

# Create the main window
window = tk.Tk()
window.title("Polynomial Regression")
window.geometry("800x900")

# Handle window close event
window.protocol("WM_DELETE_WINDOW", on_closing)

# Create a frame for the top section
top_frame = tk.Frame(window)
top_frame.pack(pady=20)

# Create a button to load data
load_button = tk.Button(
    top_frame, text="Load Data", command=load_data_and_plot, font=("Arial", 11)
)
load_button.pack(side=tk.LEFT, padx=10)

# Create a label and entry field for the degree parameter
degree_frame = tk.Frame(top_frame)
degree_frame.pack(side=tk.LEFT)
degree_label = tk.Label(degree_frame, text="Degree (1-6):", font=("Arial", 12))
degree_label.pack(side=tk.LEFT)
degree_entry = tk.Entry(degree_frame, font=("Arial", 12))
degree_entry.pack(side=tk.LEFT)

# Create a button to plot regression
plot_button = tk.Button(
    top_frame, text="Plot Regression", command=plot_loaded_data, font=("Arial", 11)
)
plot_button.pack(side=tk.LEFT, padx=10)

# Create a frame for the chart
chart_frame = tk.Frame(window)
chart_frame.pack(pady=20)

# Create an empty chart
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, chart_frame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2Tk(canvas, chart_frame)
toolbar.update()
toolbar.pack()

# Create a label to display the regression equation
equation_label = tk.Label(window, text="Regression Equation:", font=("Arial", 12))
equation_label.pack(pady=10)

bottom_frame = tk.Frame(window)
bottom_frame.pack(padx=10, pady=10)

# Create the custom x label and entry field
custom_x_label = tk.Label(bottom_frame, text="x value:", font=("Arial", 12))
custom_x_label.pack(side="left", padx=5, pady=5)

custom_x_entry = tk.Entry(bottom_frame, font=("Arial", 12))
custom_x_entry.pack(side="left", padx=5, pady=5)

# Create the "Get Custom Y" button
get_custom_y_button = tk.Button(
    bottom_frame, text="Get y value", command=get_custom_y, font=("Arial", 11)
)
get_custom_y_button.pack(side="left", padx=5, pady=5)

# Create the custom y label
custom_y_label = tk.Label(window, text="y: ", font=("Arial", 12))
custom_y_label.pack(padx=10, pady=(0, 10))


# Start the GUI event loop
window.mainloop()
