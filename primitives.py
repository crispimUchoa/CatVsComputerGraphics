from pygame.surface import Surface

color_type = str | tuple[int, int, int]
coord_type = tuple[int, int]

def set_pixel(surface: Surface, xy: coord_type, color: color_type):
    x, y = xy
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
        xy0 = vertices[i]
        xy1 = vertices[(i+1) % num_v]

        draw_bressenham_line(surface, xy0, xy1, color)

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
    
    plot8(surface, center, (x, y), color)

    while x < y:
        if d < 0:
            d+=2*x + 3
        else:
            d+=2*(x - y) + 5
            y -=1
        x+=1
        plot8(surface, center, (x, y), color)

def draw_elipse(surface: Surface, center: coord_type, a: int, b: int, color: color_type):
    x = 0
    y = b
    d = b**2 - (b + 1/4)*(a**2)
    
    #x²b² + y²a² = a²b²
    #y² = -x²b²/a² + b²
    #y = (-x²b²/a² + b²)**1/2

    #x²/a² + y²/b² = x²/r² + y²/r² => x²(1/a² - 1/r²) + y²(1/b² - 1/r²)

def flood_fill(surface: Surface, xy: coord_type, fill_color: color_type, border_color: color_type):
    width = surface.get_width()
    height = surface.get_height()

    stack = [xy, ]

    while stack:
        x, y = stack.pop()

        if not (0 <= x < width and 0 <= y < height):
            continue

        current_color = read_pixel(surface, (x, y))[:3]

        if current_color == border_color or current_color == fill_color:
            continue

        set_pixel(surface, (x, y), fill_color)
        
        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))