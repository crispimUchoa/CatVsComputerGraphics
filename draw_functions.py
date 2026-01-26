from pygame.surface import Surface

color_type = str | tuple[int, int, int]
coord_type = tuple[int, int]

def set_pixel(surface: Surface, xy: coord_type, color: color_type):
    x, y = xy
    if 0 <= 0 < surface.get_width() and 0 <= y < surface.get_height():
        surface.set_at((x,y), color)

def read_pixel(surface: Surface, xy: coord_type):
    return surface.get_at(xy)

def draw_dda_line(surface: Surface, xy0: coord_type, xy1: coord_type, color:color_type):
    x0, y0 = xy0
    x1, y1 = xy1
    dx = x1 - x0
    dy = y1 - y0

    steps = max(abs(dx), abs(dy))

    if steps > 0:
        x_inc = dx / steps
        y_inc = dy / steps

        x = x0
        y = y0

        for _ in range(steps + 1):
            set_pixel(surface, (round(x), round(y)), color)
            x += x_inc
            y += y_inc

def draw_bressenham_line(surface: Surface, xy0: coord_type, xy1: coord_type, color:color_type):
    x0, y0 = xy0
    x1, y1 = xy1
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
            set_pixel(surface, (y, x), color)
        else:
            set_pixel(surface, (x, y), color)

        if d <= 0:
            d += incE
        else:
            d += incNE
            y += ystep

        x += 1

def draw_naive_line(surface: Surface, xy0: coord_type, xy1: coord_type, color:color_type):
    x0, y0 = xy0
    x1, y1 = xy1
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
        set_pixel(surface, (x, y), color)

def draw_polygon(surface: Surface, vertices: list[coord_type], color: color_type):
    num_v = len(vertices)

    if num_v < 3:
        return

    for i in range(num_v):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i+1) % num_v]

        draw_bressenham_line(surface, (int(x0), int(y0)), (int(x1), int(y1)), color)

def plot8(surface: Surface, xyc: coord_type, xy: coord_type, color):
    xc, yc = xyc
    x, y = xy
    set_pixel(surface, (xc + x, yc + y), color)
    set_pixel(surface, (xc - x, yc + y), color)
    set_pixel(surface, (xc + x, yc - y), color)
    set_pixel(surface, (xc - x, yc - y), color)

    set_pixel(surface, (xc + y, yc + x), color)
    set_pixel(surface, (xc - y, yc + x), color)
    set_pixel(surface, (xc + y, yc - x), color)
    set_pixel(surface, (xc - y, yc - x), color)

def plot4(surface: Surface, xyc: coord_type, xy: coord_type, color):
    xc, yc = xyc
    x, y = xy

    set_pixel(surface, (xc + x, yc + y), color)
    set_pixel(surface, (xc + x, yc - y), color)
    set_pixel(surface, (xc - x, yc + y), color)
    set_pixel(surface, (xc - x, yc - y), color)



def draw_circle(surface: Surface, center: coord_type, r: int, color: color_type):
    x = 0
    y = r
    d = 1 - r
    
    incE = 2*x + 3
    incSE = 2*(x - y) + 5
    plot8(surface, center, (x, y), color)

    while x < y:
        if d < 0:
            d+= incE
        else:
            d+= incSE
            y -=1
        x+=1
        plot8(surface, center, (x, y), color)

def draw_elipse(surface: Surface, center: coord_type, a: int, b: int, color: color_type):
    a2, b2 = a*a, b*b
    x = 0
    y = b

    dx = 2*x*b2
    dy = 2*y*a2

    d1 = b2 + ( (-1)*b + 1/4)*(a2)
    
    plot4(surface, center, (x, y), color)
    while dx < dy:
        plot4(surface, center, (x, y), color)
        x+=1
        dx += 2 * b2
        if d1 < 0:
            d1 += dx + b2
        else:
            y -= 1
            dy -= 2 * a2
            d1 += dx - dy + a2
            
    d2 = b2 * (x + 1/2)**2 + a2*(y - 1)**2 - a2*b2

    while y >= 0:
        plot4(surface, center, (x, y), color)
        y -= 1
        dy -= 2 * a2

        if d2 > 0:
            d2 += a2 - dy
        else:
            x+=1
            dx += 2*b2
            d2 += dx - dy + a2

