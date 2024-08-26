import tkinter as tk
from tkinter import simpledialog, colorchooser, filedialog
from PIL import Image, ImageDraw

class PixelArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Art App")

        # Ask user for canvas size
        self.canvas_width = simpledialog.askinteger("Canvas Width", "Enter canvas width (in pixels):", minvalue=1, maxvalue=100)
        self.canvas_height = simpledialog.askinteger("Canvas Height", "Enter canvas height (in pixels):", minvalue=1, maxvalue=100)
        
        # Set the pixel size to 12:1 scale
        self.pixel_size = 12

        # Default color
        self.current_color = "black"

        # Create the canvas
        self.canvas = tk.Canvas(root, width=self.canvas_width * self.pixel_size, height=self.canvas_height * self.pixel_size)
        self.canvas.pack()

        # Create grid
        self.create_grid()

        # Color picker button
        color_button = tk.Button(root, text="Pick Color", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        # Eraser tool button
        eraser_button = tk.Button(root, text="Eraser", command=self.use_eraser)
        eraser_button.pack(side=tk.LEFT)

        # Clear button
        clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        # Save button
        save_button = tk.Button(root, text="Save", command=self.save_canvas)
        save_button.pack(side=tk.LEFT)

    def create_grid(self):
        """Create the grid for the pixel art."""
        for i in range(self.canvas_width):
            for j in range(self.canvas_height):
                self.canvas.create_rectangle(
                    i * self.pixel_size, j * self.pixel_size,
                    (i + 1) * self.pixel_size, (j + 1) * self.pixel_size,
                    outline="gray", fill="white",
                    tags=f"cell_{i}_{j}"
                )
        self.canvas.bind("<Button-1>", self.paint_pixel)

    def paint_pixel(self, event):
        """Paint the selected pixel with the current color."""
        x = event.x // self.pixel_size
        y = event.y // self.pixel_size
        self.canvas.itemconfig(f"cell_{x}_{y}", fill=self.current_color)

    def choose_color(self):
        """Choose a color using the color picker."""
        self.current_color = colorchooser.askcolor()[1]

    def use_eraser(self):
        """Set the current color to white for erasing."""
        self.current_color = "white"

    def clear_canvas(self):
        """Clear the canvas."""
        for i in range(self.canvas_width):
            for j in range(self.canvas_height):
                self.canvas.itemconfig(f"cell_{i}_{j}", fill="white")

    def save_canvas(self):
        """Save the canvas as an image."""
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("EPS files", "*.eps")])
        if file_path:
            # Create an empty PIL image and draw the canvas content onto it
            image = Image.new("RGB", (self.canvas_width * self.pixel_size, self.canvas_height * self.pixel_size), "white")
            draw = ImageDraw.Draw(image)

            for i in range(self.canvas_width):
                for j in range(self.canvas_height):
                    color = self.canvas.itemcget(f"cell_{i}_{j}", "fill")
                    if color != "white":  # Only draw colored pixels
                        x1 = i * self.pixel_size
                        y1 = j * self.pixel_size
                        x2 = x1 + self.pixel_size
                        y2 = y1 + self.pixel_size
                        draw.rectangle([x1, y1, x2, y2], fill=color)

            # Save the image in the selected format
            image.save(file_path)

# Run the app
root = tk.Tk()
app = PixelArtApp(root)
root.mainloop()
