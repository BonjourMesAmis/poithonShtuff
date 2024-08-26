import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageDraw

# Initialize the main application window
root = tk.Tk()
root.title("Paint64")

# Set up the drawing canvas
canvas_width = 800
canvas_height = 600
canvas = tk.Canvas(root, bg="white", width=canvas_width, height=canvas_height)
canvas.grid(row=0, column=0, columnspan=8)

# Variables to store the color, brush size, and current shape
current_color = "black"
brush_size = tk.IntVar(value=5)
current_shape = "freehand"

# List of 64 colors
colors = [
    "black", "gray", "red", "orange", "yellow", "green", "blue", "cyan",
    "purple", "magenta", "brown", "pink", "gold", "silver", "indigo", "lime",
    "navy", "maroon", "olive", "teal", "coral", "salmon", "turquoise", "violet",
    "chocolate", "khaki", "plum", "orchid", "peachpuff", "lavender", "sienna", "beige",
    "snow", "ghostwhite", "ivory", "linen", "honeydew", "mintcream", "azure", "aliceblue",
    "lavenderblush", "mistyrose", "seashell", "oldlace", "wheat", "lightgrey", "palegreen", "lightblue",
    "lightskyblue", "lightpink", "lightcoral", "palevioletred", "palegoldenrod", "lightyellow", "lightcyan", "lightsteelblue",
    "lemonchiffon", "lightgoldenrodyellow", "lightseagreen", "lightsalmon", "lightslategrey", "lightgreen", "lightgray", "whitesmoke"
]

# Function to change the color
def change_color(new_color):
    global current_color
    current_color = new_color

# Function to set the current shape
def set_shape(shape):
    global current_shape
    current_shape = shape

# Function to draw on the canvas
def paint(event):
    x1, y1 = (event.x - brush_size.get()), (event.y - brush_size.get())
    x2, y2 = (event.x + brush_size.get()), (event.y + brush_size.get())
    
    if current_shape == "freehand":
        canvas.create_oval(x1, y1, x2, y2, fill=current_color, outline=current_color)
    elif current_shape == "rectangle":
        canvas.create_rectangle(x1, y1, x2, y2, outline=current_color, width=brush_size.get())
    elif current_shape == "oval":
        canvas.create_oval(x1, y1, x2, y2, outline=current_color, width=brush_size.get())

# Add color buttons
for i, color in enumerate(colors):
    button = tk.Button(root, bg=color, width=3, command=lambda c=color: change_color(c))
    button.grid(row=1 + i // 8, column=i % 8)

# Add a clear button
def clear_canvas():
    canvas.delete("all")

clear_button = tk.Button(root, text="Clear", command=clear_canvas)
clear_button.grid(row=9, column=0, columnspan=2, sticky="we")

# Function to save the canvas as an image
def save_canvas():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        canvas.update()
        # Create an empty PIL image and draw the canvas content onto it
        image = Image.new("RGB", (canvas_width, canvas_height), "white")
        draw = ImageDraw.Draw(image)
        for item in canvas.find_all():
            coords = canvas.coords(item)
            if len(coords) == 4:  # oval or rectangle
                x1, y1, x2, y2 = coords
                fill_color = canvas.itemcget(item, "fill")
                outline_color = canvas.itemcget(item, "outline")
                if canvas.type(item) == "oval":
                    draw.ellipse([x1, y1, x2, y2], fill=fill_color, outline=outline_color)
                elif canvas.type(item) == "rectangle":
                    draw.rectangle([x1, y1, x2, y2], outline=outline_color)
        image.save(file_path)

save_button = tk.Button(root, text="Save", command=save_canvas)
save_button.grid(row=9, column=2, columnspan=2, sticky="we")

# Add brush size slider
brush_size_label = tk.Label(root, text="Brush Size")
brush_size_label.grid(row=9, column=4)
brush_size_slider = ttk.Scale(root, from_=1, to=20, orient=tk.HORIZONTAL, variable=brush_size)
brush_size_slider.grid(row=9, column=5, columnspan=2, sticky="we")

# Add shape buttons
freehand_button = tk.Button(root, text="Freehand", command=lambda: set_shape("freehand"))
freehand_button.grid(row=10, column=0, columnspan=2, sticky="we")

rectangle_button = tk.Button(root, text="Rectangle", command=lambda: set_shape("rectangle"))
rectangle_button.grid(row=10, column=2, columnspan=2, sticky="we")

oval_button = tk.Button(root, text="Oval", command=lambda: set_shape("oval"))
oval_button.grid(row=10, column=4, columnspan=2, sticky="we")

# Bind the paint function to the mouse movement
canvas.bind("<B1-Motion>", paint)

# Run the application
root.mainloop()
