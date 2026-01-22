from pygame.surface import Surface

color_type = str | tuple[int, int, int]

def set_pixel(surface: Surface, x: int, y: int, color: color_type):
    surface.set_at((x,y), color)

def read_pixel(surface: Surface, x: int, y: int):
    return surface.get_at((x, y))

def draw_dda_line(surface: Surface, x0:int, y0:int, x1:int, y1:int, color:color_type):
    dx = x1 - x0
    dy = y1 - y0

    steps = max(abs(dx), abs(dy))

    if steps > 0:
        x_inc = dx / steps
        y_inc = dy / steps

        x = x0
        y = y0

        for _ in range(steps + 1):
            set_pixel(surface, round(x), round(y), color)
            x += x_inc
            y += y_inc

def draw_bressenham_line(surface: Surface, x0:int, y0:int, x1:int, y1:int, color:color_type):
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0

    ystep = 1
    if dy < 0:
        ystep = -1
        dy = -dy

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x = x0
    y = y0

    while x <= x1:
        if steep:
            set_pixel(surface, y, x, color)
        else:
            set_pixel(surface, x, y, color)

        if d <= 0:
            d += incE
        else:
            d += incNE
            y += ystep

        x += 1

def draw_naive_line(surface: Surface, x0:int, y0:int, x1:int, y1:int, color:color_type):
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0

    if dx == 0:
        return
    
    m = (y1 - y0) / dx
    b = y0 - m*x0

    for x in range(x0, x1 + 1):
        y = m*x + b
        set_pixel(surface, x, y, color)

def draw_polygon(surface: Surface, vertices: list[tuple[int, int]], color: color_type):
    num_v = len(vertices)

    if num_v < 3:
        return

    for i in range(num_v):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i+1) % num_v]
        print(x1, y1)

        draw_bressenham_line(surface, x0, y0, x1, y1, color)
