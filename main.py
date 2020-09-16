#!/usr/bin/env python3
import math
from tkinter import Tk, Canvas, mainloop
from random import randrange
# 2020/09/15: Cloned. Updated to add a weighted colorization. -Rn

STAR_SIZE   = 12

COLOR_WHITE = 0
COLOR_RED   = 1
COLOR_BLUE  = 2
COLOR_GREEN = 3
COLOR_YELLOW= 4


class Star:
    __slots__ = ['x', 'y', 'z', 'id', 'radius', 'r', 'g', 'b']

    def __init__(self, x, y, z, color) -> None:
        super().__init__()
        self.id = None
        self.x = x
        self.y = y
        self.z = z
        self.radius = 1
        self.r = 255
        self.g = 255
        self.b = 255
        if color == COLOR_RED:
            self.g = 0
            self.b = 0
        elif color == COLOR_GREEN:
            self.r = 0
            self.b = 0
        elif color == COLOR_BLUE:
            self.r = 0
            self.g = 0
        elif color == COLOR_YELLOW:
            self.b = 0


class StarField:

    def __init__(self, width, height, depth=32, num_stars=500):
        self.master = Tk()
        self.master.title("StarField")
        self.master.resizable(False, False)
        self.master.maxsize(width, height)
        self.fov = 180 * math.pi / 180
        self.view_distance = 0
        self.stars = []
        self.width = width
        self.height = height
        self.max_depth = depth
        self.canvas = Canvas(self.master, width=width, height=height, bg="#000000")
        self.canvas.pack()

        for x in range(num_stars):
            color = randrange(30)
            star = Star(x=randrange(-self.width, self.width),
                        y=randrange(-self.height, self.height),
                        z=randrange(1, self.max_depth),
                        color=color)
            star.id = self.canvas.create_oval(star.x - star.radius, star.y - star.radius, star.x + star.radius, star.y + star.radius,
                                              fill='#FFFFFF')
            self.stars.append(star)
        self.draw()
        mainloop()

    def draw(self):
        for star in self.stars:
            # move depth
            star.z -= 0.19
            star.radius = (1 - float(star.z) / self.max_depth) * STAR_SIZE

            # reset depth
            if star.z <= 0:
                star.x = randrange(-self.width, self.width)
                star.y = randrange(-self.height, self.height)
                star.z = self.max_depth
                star.radius = 1

            # Transforms this 3D point to 2D using a perspective projection.
            factor = self.fov / (self.view_distance + star.z)
            x = star.x * factor + self.width / 2
            y = -star.y * factor + self.height / 2

            self.canvas.coords(star.id, x - star.radius, y - star.radius, x + star.radius, y + star.radius)
            self.canvas.itemconfig(star.id, fill='#%02x%02x%02x' % (star.r, star.g, star.b))
        self.canvas.after(30, self.draw)


if __name__ == '__main__':
    s = StarField(1290, 730)
