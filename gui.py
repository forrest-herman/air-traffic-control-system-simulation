import tkinter as tk

SIZE = 1000


# Create an instance of tkinter frame
window = tk.Tk()

# Define the geometry of window
# window.geometry("600x600")
window.config(height=SIZE, width=SIZE)
window.maxsize(SIZE, SIZE)

# Create a canvas object
canvas = tk.Canvas(window, width=SIZE, height=SIZE, bg="#5555ff")
canvas.pack(anchor='center', expand=True)

# Draw an Oval in the canvas
circle_radius = 10
x1 = (SIZE-circle_radius)/2
x2 = SIZE - x1
# canvas.create_oval(x, x, circle_radius, circle_radius, fill="white")

plane = canvas.create_oval(x1, x1, x2, x2, fill="black")
# window.update_idletasks()
# window.update()

window.after(1000, lambda: canvas.move(plane, 300, 100))


# window.update_idletasks()
# window.update()


class PlaneShape:
    def __init__(self, canvas, color, x, y):
        self.canvas = canvas
        self.plane = canvas.create_oval(x, y, x+10, y+10, fill=color)
        self.canvas.move(self.plane, 245, 100)

        self.canvas.bind("<Button-1>", self.canvas_onclick)
        self.text_id = self.canvas.create_text(300, 200, anchor='se')
        self.canvas.itemconfig(self.text_id, text='hello')

    def canvas_onclick(self, event):
        self.canvas.itemconfig(
            self.text_id,
            text="You clicked at ({}, {})".format(event.x, event.y)
        )

    def draw(self):
        self.canvas.move(self.plane, x, y)
        self.canvas.after(10, self.draw)


x = 10
y = 10
plane = PlaneShape(canvas, "black", x, y)
plane.draw()
window.mainloop()

# while(True):
#     plane = PlaneShape(canvas, "black", x, y)
#     plane.draw()
#     x = x + 1
#     y = y + 1
#     if plane.
