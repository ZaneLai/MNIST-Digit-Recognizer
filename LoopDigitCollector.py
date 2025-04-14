import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageDraw, ImageOps
import numpy as np
import pandas as pd
import os

path = "./save/handwritten_digits.csv"

class LoopDigitCollector:
    def __init__(self, master, save_path=path):
        self.master = master
        self.save_path = save_path

        self.init_csv()

        master.title("Looping Digit Collector")

        self.canvas = tk.Canvas(master, width=280, height=280, bg='white')
        self.canvas.pack()

        # Label input dropdown
        label_frame = tk.Frame(master)
        label_frame.pack()
        tk.Label(label_frame, text="Current digit:").pack(side=tk.LEFT)
        self.label_var = tk.StringVar(value="0")
        self.label_dropdown = ttk.Combobox(label_frame, textvariable=self.label_var, values=[str(i) for i in range(10)], width=5, state="readonly")
        self.label_dropdown.pack(side=tk.LEFT)

        self.button_save = tk.Button(master, text="Save Digit", command=self.save_digit)
        self.button_save.pack()

        self.button_clear = tk.Button(master, text="Clear", command=self.clear_canvas)
        self.button_clear.pack()

        self.label_info = tk.Label(master, text="Draw any digit and click 'Save Digit'", font=("Helvetica", 14))
        self.label_info.pack()

        self.image = Image.new("L", (280, 280), color=255)
        self.draw = ImageDraw.Draw(self.image)

        self.canvas.bind("<B1-Motion>", self.paint)

    def init_csv(self):
        if not os.path.exists(self.save_path):
            columns = ["label"] + [f"pixel{i}" for i in range(784)]
            df = pd.DataFrame(columns=columns)
            df.to_csv(self.save_path, index=False)

    def paint(self, event):
        x, y = event.x, event.y
        r = 8
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='black')
        self.draw.ellipse([x - r, y - r, x + r, y + r], fill=0)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw.rectangle([0, 0, 280, 280], fill=255)

    def save_digit(self):
        label = self.label_var.get() # Get the label from the dropdown

        image_resized = self.image.resize((28, 28), resample=Image.Resampling.LANCZOS)
        image_inverted = ImageOps.invert(image_resized)
        image_array = np.array(image_inverted).astype("uint8").reshape(1, -1)

        data_row = [int(label)] + image_array.flatten().tolist()
        df = pd.DataFrame([data_row])
        df.to_csv(self.save_path, mode='a', header=False, index=False)

        self.clear_canvas()

def main():
    root = tk.Tk()
    app = LoopDigitCollector(root)
    root.mainloop()

if __name__ == "__main__":
    main()