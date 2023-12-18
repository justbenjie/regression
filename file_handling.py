from tkinter import filedialog, messagebox
import pandas as pd


class FileHandler:
    def load_data(self):
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
